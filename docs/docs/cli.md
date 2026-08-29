---
icon: material/console
---

# Command line interface

The `crc` library ships with a small command line tool, which currenlty only implements one subcommand to generate CRC lookup tables.
It becomes available as `crc` as soon as the package is installed.

```console
$ crc --help
usage: crc [-h] {table} ...

A set of crc checksum related command line tools.

positional arguments:
  {table}
    table     Generates lookup tables for various crc algorithm settings

options:
  -h, --help  show this help message and exit
```

## `crc table`

Generates the lookup table for a given width and generator polynomial.

```console
$ crc table --help
usage: crc table [-h] <width> <polynomial>

positional arguments:
  <width>       width of the crc algorithm, common width's are 8, 16, 32, 64
  <polynomial>  hex value of the polynomial used for calculating the crc table

options:
  -h, --help    show this help message and exit
```

| Argument       | Description                                             |
|----------------|---------------------------------------------------------|
| `<width>`      | Width of the CRC algorithm in bits, e.g. `8`, `16`, `32`, `64` |
| `<polynomial>` | Generator polynomial as a hex value, e.g. `0x7D`        |

### Example

```console
$ crc table 8 0x7D
0x00 0x7D 0xFA 0x87 0x89 0xF4 0x73 0x0E
0x6F 0x12 0x95 0xE8 0xE6 0x9B 0x1C 0x61
0xDE 0xA3 0x24 0x59 0x57 0x2A 0xAD 0xD0
0xB1 0xCC 0x4B 0x36 0x38 0x45 0xC2 0xBF
...
```

!!! tip "Using the table from Python"

    You usually do not need to generate tables by hand. Passing
    `optimized=True` to the [`Calculator`](api/calculator.md) builds and uses a
    lookup table for you:

    ```python
    from crc import Calculator, Crc8

    calculator = Calculator(Crc8.CCITT, optimized=True)
    ```
