# Setup

## Requirements TL;DR
* [poetry](https://python-poetry.org)
* [gh](https://cli.github.com)

## 1. Install Poetry
Follow the poetry [installation instructions](https://python-poetry.org/docs/#installation).

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

1. Activate the Poetry shell

    ```
    poetry shell
    ```
  
2. Install the project dependencies
 
    ```
    poetry install
    ```

## Run the `init` task
In order to bootstrap the remaining parts of the workspace setup, just
execute the following command: 

```
invoke init
```

!!! note 

    Follow potential instructions.
