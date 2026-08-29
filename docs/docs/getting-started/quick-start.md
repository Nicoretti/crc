---
icon: material/rocket-launch-outline
---

# Quick start

This page walks you through the two things you will do most often: calculating
a checksum and verifying one.

!!! warning "Prerequisites"

    Make sure the library is [installed](installation.md).

## Calculate a checksum

Pick one of the [predefined configurations](../configurations.md), create a
[`Calculator`](../api/calculator.md) and hand it your data:

```python
from crc import Calculator, Crc8

calculator = Calculator(Crc8.CCITT)  # (1)!

checksum = calculator.checksum(b"123456789")
assert checksum == 0xF4
```

1. `Crc8.CCITT` is just one of many configurations shipping with the library.
   See [configurations](../configurations.md) for the full list of available CRC8, CRC16, CRC32 and CRC64 configurations.

## Verify a checksum

Instead of comparing checksums yourself, let the calculator do it:

```python
from crc import Calculator, Crc8

calculator = Calculator(Crc8.CCITT)

assert calculator.verify(b"123456789", 0xF4)
```

## Make it faster

Pass `optimized=True` to use a lookup table based implementation. This is the
option you want when checksumming a lot of data:

```python hl_lines="3"
from crc import Calculator, Crc8

calculator = Calculator(Crc8.CCITT, optimized=True)

assert calculator.checksum(b"123456789") == 0xF4
```

!!! warning "Create it once, reuse it"

    Building the lookup table happens when the calculator is created. Create
    the calculator once and reuse it, rather than creating a new one per
    checksum.

## Checksum a file

`checksum` and `verify` accept more than just `bytes` — a file object works
just as well, and is read in chunks so large files do not need to fit into
memory:

```python
from crc import Calculator, Crc8

calculator = Calculator(Crc8.CCITT, optimized=True)

with open("afile.txt", "rb") as f:  # (1)!
    checksum = calculator.checksum(f)
```

1. Make sure to open the file in binary mode (`"rb"`).

## Where to go next

<div class="grid cards" markdown>

-   :material-calculator: **Calculating checksums**

    ---

    All the ways to calculate and verify checksums, and which input types are
    supported.

    [:octicons-arrow-right-24: Calculating checksums](../usage/calculator.md)

-   :material-tune: **Configurations**

    ---

    Use a predefined configuration or define your own.

    [:octicons-arrow-right-24: Configurations](../usage/configurations.md)

-   :material-chip: **Raw registers**

    ---

    Drive the CRC calculation yourself for full control.

    [:octicons-arrow-right-24: Raw registers](../usage/registers.md)

</div>
