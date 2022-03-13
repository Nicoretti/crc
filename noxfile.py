from pathlib import Path

import nox

BASEPATH = Path(__file__).parent.resolve()

nox.options.sessions = ["unit", "check", "lint", "coverage"]


def _install(session):
    session.install("--upgrade", "pip")
    session.install("poetry")
    session.run("poetry", "install")


@nox.session
def coverage(session):
    _install(session)
    session.run("python", "-m", "coverage", "run", "-m", "pytest", ".")
    session.run("python", "-m", "coverage", "report", "--fail-under=99")


@nox.session
def lint(session):
    _install(session)
    session.run("python", "-m", "pylint", "--rcfile", "pylintrc", "crc.py")


@nox.session
def unit(session):
    _install(session)
    session.run("python", "-m", "pytest", ".")


@nox.session
def check(session):
    _install(session)
    session.run("python", "-m", "isort", "-v", "--check", f"{BASEPATH}")
    session.run(
        "python",
        "-m",
        "black",
        "--check",
        "--diff",
        "--color",
        f"{BASEPATH}",
    )


@nox.session
def fix(session):
    _install(session)
    session.run("python", "-m", "isort", "-v", f"{BASEPATH}")
    session.run(
        "python",
        "-m",
        "black",
        "--color",
        f"{BASEPATH}",
    )
