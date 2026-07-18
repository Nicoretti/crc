"""camas task definitions for the crc project.

Migrated from invoke. camas is the single source of truth: the same tree drives
local development and CI, and ``camas matrix`` reproduces the CI Python matrix.
"""

from camas import (
    Claude,
    Config,
    Parallel,
    Sequential,
    Task,
    by_suffix,
)

py_files = by_suffix((".py",), default=("src", "test", "docs", "tasks.py"))

isort = Task("uv run isort {paths}", mutates=True, paths=py_files)
black = Task("uv run black {paths}", mutates=True, paths=py_files)
fix = Sequential(isort, black, name="fix")

isort_check = Task("uv run isort --check --diff {paths}", paths=py_files)
black_check = Task("uv run black --check --diff {paths}", paths=py_files)
format_check = Parallel(isort_check, black_check)

lint = Task("uv run pylint {paths}", paths="src")
typing = Task("uv run mypy {paths}", paths="src")

test = Task("uv run pytest test/unit test/integration")
coverage = Sequential(
    Task("uv run coverage run -m pytest test/unit test/integration"),
    Task("uv run coverage report --fail-under=100 --show-missing"),
)

docs = Task(
    "uv run mkdocs build -c -s -d ../.html-documentation -f docs/mkdocs.yml",
    when="docs",
)

init = Task("uv run pre-commit install")

release_prepare = Sequential(
    Task("uv run hatch version {VERSION}"),
    Task("git add pyproject.toml"),
    Task('git commit -m "Prepare release {VERSION}"'),
    matrix={"VERSION": ("",)},
)
release_workflow = Sequential(
    Task("git tag {VERSION}"),
    Task("git push origin {VERSION}"),
    matrix={"VERSION": ("",)},
)

check = Parallel(format_check, lint, typing, test)
all = Sequential(fix, check)

matrix = Sequential(
    Task("uv sync"),
    check,
    env={"UV_PROJECT_ENVIRONMENT": ".camas/.venv-{PY}", "UV_PYTHON": "{PY}"},
    matrix={"PY": ("3.8", "3.9", "3.10", "3.11", "3.12", "3.13")},
)

_ = Config(default_task=all, github_task=check, agent=Claude(fix=fix, check=check))
