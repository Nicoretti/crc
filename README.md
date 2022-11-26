# Summary

Library and CLI tool for calculating and verifying CRC checksums.

[![CI](https://github.com/Nicoretti/crc/actions/workflows/ci.yml/badge.svg)](https://github.com/Nicoretti/crc/actions/workflows/unit.yaml)
[![coveralls](https://coveralls.io/repos/github/Nicoretti/crc/badge.svg?branch=master)](https://coveralls.io/github/Nicoretti/crc)
[![python](https://img.shields.io/pypi/pyversions/crc)](https://pypi.org/project/crc/)
[![pypi](https://img.shields.io/pypi/v/crc)](https://pypi.org/project/crc/)
[![downloads](https://img.shields.io/pypi/dm/crc)](https://pypi.org/project/crc/)
[![license](https://img.shields.io/pypi/l/crc)](https://opensource.org/licenses/BSD-2-Clause)

## Provided Default Configuration(s) of CRC Algorithms:

| CRC8 | CRC16 | CRC32 | CRC64 |
|------|-------|-------|-------|
| CCITT | CCITT | CRC32 | CRC64 |
| AUTOSAR | GSM | AUTOSAR | |
| SAJ1850 | PROFIBUS | BZIP2 | |
| BLUETOOTH | | POSIX | |
| MAXIM-DOW | | | | |

## Requirements
* Python 3.7 and newer

## Examples

### Calculate crc using the `Calculator`

```python
from crc import Calculator, Crc8

data = bytes([0, 1, 2, 3, 4, 5])
expected = 0xBC
calculator = Calculator(Crc8.CCITT)

assert expected == calculator.checksum(data)
assert calculator.verify(data, expected)
```

### Speed up the calculation by using a optimized crc `Calculator`

```python
from crc import Calculator, Crc8

data = bytes([0, 1, 2, 3, 4, 5])
expected = 0xBC
calculator = Calculator(Crc8.CCITT, optimized=True)

assert expected == calculator.checksum(data)
assert calculator.verify(data, expected)
```

### Create a custom crc configuration for the crc calculation

```python
from crc import Calculator, Configuration

data = bytes([0, 1, 2, 3, 4, 5])
expected = 0xBC

calculator = Calculator(
    Configuration(
        width=8,
        poly=0x07,
        init_value=0x00,
        final_xor_value=0x00,
        reverse_input=False,
        reverse_output=False
    ),
    optimized=True
)

assert expected == calculator.checksum(data)
assert calculator.verify(data, expected)
```

### Use bare bones crc registers

```python
from crc import Crc8, TableBasedRegister, Register

data = bytes([0, 1, 2, 3, 4, 5])
expected = 0xBC

register = Register(Crc8.CCITT)
register.init()
register.update(data)
assert expected == register.digest()

register = TableBasedRegister(Crc8.CCITT)
register.init()
register.update(data)
assert expected == register.digest()
```

## Command line tool
See `crc --help`

### subcommand(s)
#### table
Subcommand to pre-compute crc lookup tables. See also `crc table --help`.
#### checksum
Subcommand to calculate crc checksums of input file(s). See also `crc checksum --help`.

References & Resources
-----------------------
* [A Painless guide to crc error detection algorithms](http://www.zlib.net/crc_v3.txt)
* [Project on Github](https://github.com/Nicoretti/crc)
* [CRC-Catalogue](http://reveng.sourceforge.net/crc-catalogue/all.htm)

