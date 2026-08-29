---
title: CRC
icon: material/home
---

# CRC

A pure Python library to calculate and verify CRC checksums.

[![Checks](https://img.shields.io/github/checks-status/nicoretti/crc/master?style=flat-square&labelColor=414a52&color=00796b#only-light)](https://github.com/Nicoretti/crc/actions)
[![Coverage](https://img.shields.io/coverallsCoverage/github/Nicoretti/crc?style=flat-square&labelColor=414a52&color=00796b#only-light)](https://coveralls.io/github/Nicoretti/crc)
[![License](https://img.shields.io/pypi/l/crc?style=flat-square&labelColor=414a52&color=00796b#only-light)](https://opensource.org/licenses/BSD-2-Clause)
[![Downloads](https://img.shields.io/pypi/dm/crc?style=flat-square&labelColor=414a52&color=00796b#only-light)](https://pypi.org/project/crc/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/crc?style=flat-square&labelColor=414a52&color=00796b#only-light)](https://pypi.org/project/crc/)
[![PyPi Package](https://img.shields.io/pypi/v/crc?style=flat-square&labelColor=414a52&color=00796b#only-light)](https://pypi.org/project/crc/)
[![Checks](https://img.shields.io/github/checks-status/nicoretti/crc/master?style=flat-square&labelColor=444c56&color=00857a#only-dark)](https://github.com/Nicoretti/crc/actions)
[![Coverage](https://img.shields.io/coverallsCoverage/github/Nicoretti/crc?style=flat-square&labelColor=444c56&color=00857a#only-dark)](https://coveralls.io/github/Nicoretti/crc)
[![License](https://img.shields.io/pypi/l/crc?style=flat-square&labelColor=444c56&color=00857a#only-dark)](https://opensource.org/licenses/BSD-2-Clause)
[![Downloads](https://img.shields.io/pypi/dm/crc?style=flat-square&labelColor=444c56&color=00857a#only-dark)](https://pypi.org/project/crc/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/crc?style=flat-square&labelColor=444c56&color=00857a#only-dark)](https://pypi.org/project/crc/)
[![PyPi Package](https://img.shields.io/pypi/v/crc?style=flat-square&labelColor=444c56&color=00857a#only-dark)](https://pypi.org/project/crc/)



## What it does

```python
from crc import Calculator, Crc8

calculator = Calculator(Crc8.CCITT)

calculator.checksum(b"123456789")      # (1)!
calculator.verify(b"123456789", 0xF4)  # (2)!
```

1. Returns the checksum as an `int`, here `0xF4`.
2. Returns `True` if the data matches the expected checksum.

## Why use it

<div class="grid cards" markdown>

-   :simple-python: **No dependencies**

    ---

    Does not contribute to potentional dependency conflicts, easy to vendor if needed.

    
-   :material-book-open-variant: **Batteries included**

    ---

    More than 20 predefined configurations, plus support for custom configurations.

-   :material-devices: **Portable**

    ---

    As pure Python library with no native dependencies it runs wherever a python runs.

-   :material-file-tree: **Flexible input**

    ---

    Works with `bytes`, `int`, `files`, `streams`, `iterables` and anything
    convertible to `bytes`.

</div>

## Where to go next

<div class="grid cards" markdown>

-   :material-rocket-launch: **Getting started**

    ---

    Install the library and calculate your first checksum.

    [:octicons-arrow-right-24: Getting started](getting-started/installation.md)

-   :material-school: **Usage guide**

    ---

    Task oriented guides for calculating, verifying and configuring CRCs.

    [:octicons-arrow-right-24: Usage guide](usage/calculator.md)

-   :material-table: **Configurations**

    ---

    Browse every CRC configuration that ships with the library, including all
    of their parameters.

    [:octicons-arrow-right-24: Configurations](configurations.md)

-   :material-api: **API reference**

    ---

    Detailed documentation for the `Calculator`, `Configuration` and the
    low level register types.

    [:octicons-arrow-right-24: API reference](api/calculator.md)

-   :material-console: **Command line**

    ---

    Generate CRC lookup tables straight from your terminal with the bundled
    `crc` command.

    [:octicons-arrow-right-24: CLI](cli.md)

-   :material-hammer-wrench: **Development**

    ---

    Set up a development environment and learn how to contribute.

    [:octicons-arrow-right-24: Development](development/index.md)

</div>

## Project links

<div class="grid cards" markdown>

-   :simple-github: **Source code**

    ---

    [github.com/Nicoretti/crc](https://github.com/Nicoretti/crc)

-   :simple-pypi: **Package**

    ---

    [pypi.org/project/crc](https://pypi.org/project/crc/)

-   :material-bug: **Issues**

    ---

    [Report a bug or request a feature](https://github.com/Nicoretti/crc/issues)

-   :material-scale-balance: **License**

    ---

    [BSD-2-Clause](https://opensource.org/licenses/BSD-2-Clause)

</div>

## References & resources

- [A painless guide to CRC error detection algorithms](http://www.zlib.net/crc_v3.txt)
- [CRC catalogue](http://reveng.sourceforge.net/crc-catalogue/all.htm)
