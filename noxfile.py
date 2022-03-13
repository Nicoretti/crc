import tempfile

import nox
from pathlib import Path

nox.sessions = ['unit', 'lint', 'coverage']


def _install(session):
    session.install('--upgrade', 'pip')
    session.install('poetry')
    session.run('poetry', 'install')


@nox.session
def coverage(session):
    _install(session)
    session.run('python', '-m', 'coverage', 'run', '--source=crc', '-m', 'pytest', '.')
    session.run('python', '-m', 'coverage', 'report', '--fail-under=99')


@nox.session
def lint(session):
    _install(session)
    session.run('python', '-m', 'pylint', '--rcfile', 'pylintrc', 'crc.py')


@nox.session
def unit(session):
    _install(session)
    session.run('python', '-m', 'pytest', '.')
