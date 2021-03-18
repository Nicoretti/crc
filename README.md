# Overview
[![travis-ci](https://travis-ci.org/Nicoretti/crc.svg?branch=master)](https://travis-ci.org/Nicoretti/crc)
[![appveyor](https://ci.appveyor.com/api/projects/status/1tkrwbp3tiv0ikib/branch/master?svg=true)](https://ci.appveyor.com/project/Nicoretti/crc)
[![coveralls](https://coveralls.io/repos/github/Nicoretti/crc/badge.svg?branch=master)](https://coveralls.io/github/Nicoretti/crc)


Library and CLI tool for calculating and verifying CRC checksums.

## Provided Default Configuration(s) of CRC Algorithms:

| CRC8 | CRC16 | CRC32 | CRC64 |
|------|-------|-------|-------|
| CCITT | CCITT | CRC32 | CRC64 |
| AUTOSAR | GSM | AUTOSAR | |
| SAJ1850 | PROFIBUS | BZIP2 | |
| BLUETOOTH | | POSIX | |

## Requirements
* Python 3.6 and newer
* docopt >= 0.6.2

## Examples

### Calculate crc using the `CrcCalculator`
```python
from crc.crc import CrcCalculator, Crc8
data = [0, 1, 2, 3, 4, 5 ]
expected_checksum = 0xff
crc_calculator = CrcCalculator(Crc8.CCITT)

checksum = crc_calculator.calculate_checksum(data)

assert checksum == expected_checksum
assert crc_calculator.verify_checksum(data, expected_checksum)
```

### Speed up the calculation by using a table based `CrcCalculator`
```python
from crc.crc import CrcCalculator, Crc8

data = [0, 1, 2, 3, 4, 5 ]
expected_checksum = 0xff
use_table = True
crc_calculator = CrcCalculator(Crc8.CCITT, use_table)

checksum = crc_calculator.calculate_checksum(data)

assert checksum == expected_checksum
assert crc_calculator.verify_checksum(data, expected_checksum)
```

### Create a custom crc configuration for the crc calculation 
```python
from crc.crc import CrcCalculator, Configuration

data = [0, 1, 2, 3, 4, 5 ]
expected_checksum = 0xff

width = 8
poly=0x07,
init_value=0x00,
final_xor_value=0x00,
reverse_input=False,
reverse_output=False
configuration = Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)

use_table = True
crc_calculator = CrcCalculator(configuration, use_table)

checksum = crc_calculator.calculate_checksum(data)
assert checksum == expected_checksum
assert crc_calculator.verify_checksum(data, expected_checksum)
```

### Use bare bones crc registers
```python
from crc.crc import Crc8, TableBasedCrcRegister, CrcRegister

data = [0, 1, 2, 3, 4, 5 ]
expected_checksum = 0xff

reg = CrcRegister(Crc8.CCITT)
table_reg = TableBasedCrcRegister(Crc8.CCITT)

reg.init()
reg.update(data)
assert expected_checksum == reg.digest()

table_reg.init()
table_reg.update(data)
assert expected_checksum == table_reg.digest()
```

## Command line tools

### cli extension point
* `crc.cli.command`

### crc
A set of crc checksum related command line tools.

```
    usage:
        crc [--version][--help] <command> [<args>...]

    options:

        -h, --help      prints this help dialoge
        --version       version

    commands:
        table       creates a crc lookup table.
        verfiy      verfies a already calcualted crc for the specified data.
        calcualte   calculates the crc checksum for the specified data.
```

#### subcommand table
Command line tool to create crc lookup tables.
```
    usage:
        crc table [options] <width> <polynom>

    arguments:
        <polynom>       hex value of the polynom used for calculating the crc table.

    options:
        -h, --help
        --version
```

References & Resources
-----------------------
* [A Painless guide to crc error detection algorithms](http://www.zlib.net/crc_v3.txt)
* [Project on Github](https://github.com/Nicoretti/crc)
* [CRC-Catalouge](http://reveng.sourceforge.net/crc-catalogue/all.htm)

