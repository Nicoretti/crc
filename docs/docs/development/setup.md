# Setup

## Requirements TL;DR
* [uv](https://docs.astral.sh/uv/)
* [gh](https://cli.github.com)

## 1. Install Poetry
Follow the uv [installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

## 2. Install gh
Follow the gh [installation instructions](https://cli.github.com).

## 3. Checkout the project


=== "GitHub CLI"

    ```
    gh repo clone Nicoretti/crc
    ```

=== "SSH"

    ```
    git clone git@github.com:Nicoretti/crc.git
    ```

=== "HTTPS"

    ```
    git clone https://github.com/Nicoretti/crc.git
    ```

## 4. Switch into the directory

```
cd crc
```

## 5. The Poetry environment
Make sure the poetry environment is setup properly and all dependencies are installed.

1. Sync the UV environment

    ```
    uv sync
    ```

2. Activate the uv managed virtual environment

    ```
    source activate .venv/bin/activate
    ```

## Run the `init` task
In order to bootstrap the remaining parts of the workspace setup, just
execute the following command:

```
uv run invoke init
```

!!! note

    Follow potential instructions.
