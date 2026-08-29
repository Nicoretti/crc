---
icon: material/hammer-wrench
---

# Setup

## Requirements

| Tool                                     | Purpose                            |
|------------------------------------------|------------------------------------|
| [uv](https://docs.astral.sh/uv/)         | Environment and dependency manager |
| [gh](https://cli.github.com)             | GitHub CLI, used for releases      |
| [git](https://git-scm.com)               | Version control                    |

## 1. Install the tooling

=== "uv"

    Follow the uv [installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

=== "gh"

    Follow the gh [installation instructions](https://cli.github.com).

## 2. Check out the project

=== "GitHub CLI"

    ```shell
    gh repo clone Nicoretti/crc
    ```

=== "SSH"

    ```shell
    git clone git@github.com:Nicoretti/crc.git
    ```

=== "HTTPS"

    ```shell
    git clone https://github.com/Nicoretti/crc.git
    ```

Then switch into the project directory:

```shell
cd crc
```

## 3. Create the environment

Make sure the environment is set up properly and all dependencies are installed:

```shell
uv sync
```

Optionally activate the virtual environment managed by uv:

```shell
source .venv/bin/activate
```

!!! tip

    Activating is not strictly necessary, prefixing commands with `uv run`
    works just as well, e.g. `uv run invoke test.unit`.

## 4. Bootstrap the workspace

To bootstrap the remaining parts of the workspace setup (git hooks, checks that
required tools are available, ...), run:

```shell
uv run invoke init
```

!!! note

    Follow potential instructions printed by the task.

## Common tasks

All automation is exposed through [invoke](https://www.pyinvoke.org) tasks.
Run `uv run invoke --list` to see everything that is available.

=== "Tests"

    ```shell
    invoke test.unit          # run the unit tests
    invoke test.integration   # run the integration tests
    invoke test.coverage      # run all tests and report coverage
    ```

=== "Checks"

    ```shell
    invoke format             # format the code
    invoke check.format       # verify formatting
    invoke check.lint         # run the linter
    invoke check.typing       # run the type checker
    ```

=== "Documentation"

    ```shell
    invoke docs.serve         # live preview of the documentation
    invoke docs.build         # build the documentation
    docs.generate (docs.gen)  # Generate dynamic documentation content (e.g. configurations.md)
    invoke docs.clean         # remove build artifacts
    ```

## Documentation

The documentation is built with [Zensical](https://zensical.org) and lives in
the `docs/` directory:

| Path                       | Content                                            |
|----------------------------|----------------------------------------------------|
| `zensical.toml`            | Site configuration (nav, theme, plugins)           |
| `docs/docs/`               | The Markdown sources of the documentation          |
| `docs/overrides/`          | Theme template overrides                           |
| `docs/overrides/.icons/`   | Custom icons, e.g. the project logo                |
| `docs/docs/stylesheets/`   | Additional stylesheets                             |
| `docs/docs/assets/images/` | Images and the favicon                             |
| `docs/scripts/`            | Scripts generating documentation content           |

Start a live preview with:

```shell
invoke docs.serve
```

!!! note "Generated content"

    The `configurations.md` page is generated from the source code by
    `docs/scripts/configurations.py`. It is regenerated automatically by the
    `docs.build` and `docs.serve` tasks, and is therefore not checked in.
