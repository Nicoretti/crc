from pathlib import Path

import nox

BASEPATH = Path(__file__).parent.resolve()

nox.options.sessions = ["unit", "check", "lint", "coverage"]


@nox.session(python=False)
def coverage(session):
    session.run(
        "poetry",
        "run",
        "python",
        "-m",
        "coverage",
        "run",
        "-m",
        "pytest",
        f"{BASEPATH}",
    )
    session.run(
        "poetry", "run", "python", "-m", "coverage", "report", "--fail-under=98"
    )


@nox.session(python=False)
def lint(session):
    session.run("poetry", "run", "python", "-m", "pylint", "crc.py")


@nox.session(python=False)
def unit(session):
    session.run("poetry", "run", "python", "-m", "pytest", ".")


@nox.session(python=False)
def check(session):
    session.run(
        "poetry", "run", "python", "-m", "isort", "-v", "--check", f"{BASEPATH}"
    )
    session.run(
        "poetry",
        "run",
        "python",
        "-m",
        "black",
        "--check",
        "--diff",
        "--color",
        f"{BASEPATH}",
    )


@nox.session(python=False)
def fix(session):
    session.run("poetry", "run", "python", "-m", "isort", "-v", f"{BASEPATH}")
    session.run(
        "poetry",
        "run",
        "python",
        "-m",
        "black",
        "--color",
        f"{BASEPATH}",
    )


@nox.session(python=False)
def release(session):
    if not session.posargs:
        session.error("No versio argument specified")
    version = session.posargs[0]
    session.run("poetry", "version", version)
    session.run("git", "add", ".")
    session.run("git", "commit")
    session.run("git", "tag", version)
    session.run("poetry", "publish")
    session.run("git", "push")
    session.run("git", "push", "origin", version)
