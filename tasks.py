"""Automation tasks for the crc project"""

import shutil
import sys
from functools import partial
from inspect import cleandoc
from pathlib import Path
from shutil import which
from typing import Iterable

from invoke import (
    Collection,
    task,
)
from invoke.main import program

BASEPATH = Path(__file__).parent.resolve()


def _python_files(
    project_root: Path, path_filters: Iterable[str] = ("dist", ".eggs", "venv")
) -> Iterable[Path]:
    """Returns all relevant"""
    return _deny_filter(project_root.glob("**/*.py"), deny_list=path_filters)


def _deny_filter(files: Iterable[Path], deny_list: Iterable[str]) -> Iterable[Path]:
    """
    Adds a filter to remove unwanted paths containing python files from the iterator.
     args:
     return:
    """
    for entry in deny_list:
        files = filter(lambda path: entry not in path.parts, files)
    return files


def _cmd(*args):
    return " ".join(args)


def _poetry(*args):
    return _cmd("poetry", "run", *args)


def _select_files(root, files):
    if root != BASEPATH and files is not None:
        raise Exception(
            "Conflicting options --files --root, details: "
            "either specify --files or --root but not both."
        )
    return (
        list(files)
        if files is not None and len(files) > 0
        else [f"{f}" for f in _python_files(BASEPATH)]
    )


def _is_command_available(command: str) -> bool:
    path = which(command)
    return path is not None and path not in ["", " "]


class Console:
    stdout = print
    stderr = partial(print, file=sys.stderr)


@task(aliases=["init"])
def initialize_workspace(context):
    """
    Prepare/Initialize the workspace
    """
    context.run("pre-commit install")
    if not _is_command_available("gh"):
        Console.stdout(
            cleandoc(
                """
            ❌  Error
            Please install the gh command line tool, and then rerun this task.
            Details: https://cli.github.com/manual/installation
            """
            )
        )
        sys.exit(-1)
    result = context.run(_cmd("gh", "auth", "status"), warn=True, pty=True)
    if not result.ok:
        Console.stdout(
            cleandoc(
                """
            ❌  Error
            Please authenticate the gh command line tool, and then rerun this task.
            Details see: gh auth -h
            """
            )
        )
        sys.exit(-1)
    Console.stdout("✅  You are all set, happy hacking!")


@task(
    name="format",
    optional=["root", "files", "fix"],
    iterable=["files"],
    help={
        "root": f"default: {BASEPATH}",
        "fix": "default: True",
        "files": "default: None",
    },
    aliases=["fmt"],
)
def fmt(context, root=BASEPATH, files=None, fix=True):
    """Run code formatter(s)"""
    mode_filter = lambda v: v != "--check" if fix else lambda v: True
    files = _select_files(root, files)
    isort = _poetry(*filter(mode_filter, ["isort", "--check", "-v"]), *files)
    black = _poetry(*filter(mode_filter, ["black", "--check", "--color"]), *files)
    context.run(isort)
    context.run(black)


@task(aliases=["ut"])
def unit_test(context, root=BASEPATH / "test" / "unit", coverage=False):
    """Run all unit tests"""
    command = ["coverage", "run", "-m", "-a"] if coverage else []
    command = _poetry(*command, "pytest", f"{root}")
    context.run(command)


@task(aliases=["it"])
def integration_test(context, root=BASEPATH / "test" / "integration", coverage=False):
    """Run all integration tests"""
    command = ["coverage", "run", "-m", "-a"] if coverage else []
    command = _poetry(*command, "pytest", f"{root}")
    context.run(command)


@task(
    optional=["root"],
    help={"root": f"default: {BASEPATH}"},
    aliases=["cov"],
)
def coverage(context, root=BASEPATH):
    """Run all tests and collect & report coverage information"""
    coverage_file = BASEPATH / ".coverage"
    coverage_file.unlink(missing_ok=True)
    unit_test(context, root=root / "test" / "unit", coverage=True)
    integration_test(context, root=root / "test" / "integration", coverage=True)
    report = _poetry("coverage", "report", "--fail-under=100", "--show-missing")
    context.run(report)


@task(
    optional=["root", "files"],
    iterable=["files"],
    help={
        "root": f"default: {BASEPATH}",
        "files": "default: None",
    },
)
def lint(context, root=BASEPATH, files=None):
    """Run linting"""
    files = _select_files(root, files)
    pylint = _poetry("pylint", *files)
    context.run(pylint)


@task(
    optional=["root", "files"],
    iterable=["files"],
    help={
        "root": f"default: {BASEPATH}",
        "files": "default: None",
    },
)
def typing(context, root=BASEPATH, files=None):
    """Run type check(s)"""
    files = _select_files(root, files)
    mypy = _poetry("mypy", *files)
    context.run(mypy)


@task(
    optional=["root", "files"],
    iterable=["files"],
    help={
        "root": f"default: {BASEPATH}",
        "files": "default: None",
    },
)
def check(context, root=BASEPATH, files=None):
    """Run all code format checks"""
    fmt(context, root, files, fix=False)


@task
def clean_docs(_context):
    """Remove all documentation build artifacts"""
    doc_output_folder = BASEPATH / ".html-documentation"
    if doc_output_folder.exists():
        shutil.rmtree(doc_output_folder)


@task
def build_docs(context):
    """Build project documentation"""
    context.run(
        _poetry(
            "mkdocs",
            "build",
            "-c",
            "-s",
            "-d",
            f"{BASEPATH / '.html-documentation'}",
            "-f",
            f"{BASEPATH / 'docs' / 'mkdocs.yml'}",
        )
    )


@task
def serve_docs(context):
    """Serve project documentation"""
    context.run(_poetry("mkdocs", "serve", "-f", f"{BASEPATH / 'docs' / 'mkdocs.yml'}"))


@task
def release_pypi(context):
    """Create a PyPi release"""
    context.run(_cmd("poetry", "build"))
    context.run(_cmd("poetry", "publish"))


@task(aliases=["gh"])
def release_github(context, version):
    """Create a GitHub release"""
    context.run(_cmd("poetry", "build"))
    context.run(_cmd("gh", "release", "create", version, "--title", version, "dist/*"))


@task
def release_docs(context):
    """Deploy documentation to GitHub pages"""
    context.run(
        _poetry(
            "mkdocs",
            "deploy",
            "-f",
            f"{BASEPATH / 'docs' / 'mkdocs.yml'}",
            "--remote-branch",
            "gh-pages",
        )
    )


@task(aliases=["prep"])
def release_prepare(context, version):
    """Pre release steps"""
    answer = input("did you update the changelog? [y/n] ").lower()
    if answer not in ["yes", "y"]:
        Console.stdout("Aborting, re run once the changelog have been updated.")
        sys.exit(-1)
    context.run(_cmd("poetry", "version", version))
    context.run(_cmd("git", "add", "pyproject.toml"))
    context.run(_cmd("git", "commit", "-m", f'"Prepare release {version}"'))


@task
def release_workflow(context, version):
    """Start/Trigger a GitHub action based release workflow"""
    context.run(_cmd("git", "tag", version))
    context.run(_cmd("git", "push", "origin", version))
    context.run(_cmd("gh", "workflow", "view", "ci-cd.yml", "--web"))


@task
def release_local(context, version):
    """Do a release out of the current workspace"""
    check(context)
    lint(context)
    typing(context)
    coverage(context)
    release_prepare(context, version)
    release_github(context, version)
    release_pypi(context)
    release_docs(context)


test = Collection("test")
test.add_task(unit_test, name="unit")
test.add_task(integration_test, name="integration")
test.add_task(coverage, name="coverage")

checks = Collection("check")
checks.add_task(lint, name="lint")
checks.add_task(typing, name="typing")
checks.add_task(check, name="format")

docs = Collection("docs")
docs.add_task(clean_docs, name="clean")
docs.add_task(build_docs, name="build")
docs.add_task(serve_docs, name="serve")

release = Collection("release")
release.add_task(release_prepare, name="prepare")
release.add_task(release_workflow, name="workflow")
release.add_task(release_local, name="local")
release.add_task(release_pypi, name="pypi")
release.add_task(release_github, name="github")
release.add_task(release_docs, name="docs")

namespace = Collection()
namespace.add_task(initialize_workspace)
namespace.add_task(fmt, name="format")
namespace.add_collection(test)
namespace.add_collection(checks)
namespace.add_collection(docs)
namespace.add_collection(release)

if __name__ == "__main__":
    program.run()
