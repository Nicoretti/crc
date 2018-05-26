# Status

![https://travis-ci.org/Nicoretti/crc](https://travis-ci.org/Nicoretti/crc.svg?branch=master)
![https://ci.appveyor.com/project/Nicoretti/crc](https://ci.appveyor.com/api/projects/status/1tkrwbp3tiv0ikib/branch/master?svg=true)
![https://coveralls.io/github/Nicoretti/crc?branch=master](https://coveralls.io/repos/Nicoretti/crc/badge.svg?branch=master&service=github)
![https://landscape.io/github/Nicoretti/crc/master](https://landscape.io/github/Nicoretti/crc/master/landscape.svg?style=flat)
![http://py-crc.readthedocs.org/en/latest/?badge=latest](https://readthedocs.org/projects/py-crc/badge/?version=latest)
![https://gemnasium.com/Nicoretti/crc](https://gemnasium.com/Nicoretti/crc.svg)

# Overview
The crc package provides provides support for the most common functionality to handle and calculate various kinds of crc checksums.
(e.g. Crc8, Crc16, Crc32)

## Supported CRC Algorithms:
TBD

## Requirements
* Python 3.6 and newer


## Usage

### Calculate and verify crc checksum using provided crc algorithm
```python
data = [0, 1, 2, 3, 4, 5 ]
expected_checksum = 0xff
crc_calculator = CrcCalculator(Crc8.CCITT)

checksum = crc_calculator.calculate_checksum(data)

assert checksum == expected_checksum
assert crc_calculator.verfify_checksum(data, expected_checksum)
```

### Calculate crc using the CrcRegister class
```python
data = [0, 1, 2, 3, 4, 5 ]
expected_checksum = 0xff
crc_calculator = CrcCalculator(Crc8.CCITT)
```

### Speed up calculation (TableBasedRegister)
```python
data = [0, 1, 2, 3, 4, 5 ]
expected_checksum = 0xff
crc_calculator = CrcCalculator(Crc8.CCITT)
```

### How to create a custom crc configuration
```python
data = [0, 1, 2, 3, 4, 5 ]
expected_checksum = 0xff
crc_calculator = CrcCalculator(Crc8.CCITT)
```

### Write your own CrcRegister based on CrcRegisterBase

#### Based on CrcRegisterBase

```python
data = [0, 1, 2, 3, 4, 5 ]
expected_checksum = 0xff
crc_calculator = CrcCalculator(Crc8.CCITT)
```
.. code-block::


#### Based on AbstractCrcRegister
```python
data = [0, 1, 2, 3, 4, 5 ]
expected_checksum = 0xff
crc_calculator = CrcCalculator(Crc8.CCITT)
```


## Command line tools

### cli extension point
name:  crc.cli.command
description: TBD

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

table
-----
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

Tips & Tricks
-------------
Info:
Main code -> crc.py works without any dependencies -> copy and paste into project
but gererally highly recommend -> install using pip -> tests etc


References & Resources
-----------------------
* [A Painless guide to crc error detection algorithms](http://www.zlib.net/crc_v3.txt)
* [Project on Github](https://github.com/Nicoretti/crc)
* [CRC-Catalouge](http://reveng.sourceforge.net/crc-catalogue/all.htm)

