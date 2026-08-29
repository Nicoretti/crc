---
icon: material/download
---

# Installation

=== "pip"

    ```shell
    pip install crc
    ```

=== "uv"

    ```shell
    uv add crc
    ```

=== "poetry"

    ```shell
    poetry add crc
    ```

## Requirements

| Requirement | Version                                        |
|-------------|------------------------------------------------|
| Python      | >= [3.11](https://www.python.org)              |

## Verify the installation

```console
$ python -c "import crc; print(crc.__name__)"
crc
```

The installation also provides the `crc` command line tool:

```console
$ crc --help
```

[:octicons-arrow-right-24: Command line interface](../cli.md)

## Next steps

<div class="grid cards" markdown>

-   :material-rocket-launch: **Quick start**

    ---

    Calculate and verify your first checksum in a couple of lines.

    [:octicons-arrow-right-24: Quick start](quick-start.md)

-   :material-school: **Usage guide**

    ---

    Learn about configurations, input types and raw registers.

    [:octicons-arrow-right-24: Usage guides](../usage/index.md)

</div>
