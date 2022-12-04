<h1 align="center">CRC</h1>
<p align="center">

Calculate CRC checksums, verify CRC checksum, predefined CRC configurations, custom CRC configurations
</p>

<p align="center">

<a href="https://github.com/Nicoretti/crc/actions/workflows/pr-merge.yml">
    <img src="https://img.shields.io/github/workflow/status/Nicoretti/crc/PR-Merge/master" alt="Test">
</a>
<a href="https://coveralls.io/github/Nicoretti/crc">
    <img src="https://img.shields.io/coverallsCoverage/github/Nicoretti/crc" alt="Coverage">
</a>
<a href="https://opensource.org/licenses/BSD-2-Clause">
    <img src="https://img.shields.io/pypi/l/crc" alt="License">
</a>
<a href="https://pypi.org/project/crc/">
    <img src="https://img.shields.io/pypi/dm/crc" alt="Downloads">
</a>
<a href="https://pypi.org/project/crc/">
    <img src="https://img.shields.io/pypi/pyversions/crc" alt="Supported Python Versions">
</a>
<a href="https://pypi.org/project/crc/">
    <img src="https://img.shields.io/pypi/v/crc" alt="PyPi Package">
</a>
</p>

---
* Documentation: [https://nicoretti.github.io/crc](https://nicoretti.github.io/crc)
* Source Code: [https://github.com/Nicoretti/crc](https://github.com/Nicoretti/crc)
* Release Notes: [https://nicoretti.github.io/crc/release-notes](https://nicoretti.github.io/crc/release-notes)
---

## Available CRC Configurations
For convince various frequently used crc configurations ship with the library out of the box.

| CRC8 | CRC16 | CRC32 | CRC64 |
|------|-------|-------|-------|
| CCITT | CCITT | CRC32 | CRC64 |
| AUTOSAR | GSM | AUTOSAR | |
| SAJ1850 | PROFIBUS | BZIP2 | |
| BLUETOOTH | | POSIX | |
| MAXIM-DOW | | | | |

If you find yourself in the position, where having a new configuration available out of the
box would be desirable, feel free to create a [PR](https://github.com/Nicoretti/crc/pulls) or file an [issue](https://github.com/Nicoretti/crc/issues).

## Custom Configurations

If you want to create a custom configuration, you should have the following information available:

🗒 Note: 

    This library currently only supports bit widths of full bytes 8, 16, 24, 32, ...

* **width**
* **polynom**
* **init value**
* **final xor value**
* **reversed input**
* **reversed output**

In case you only have a name of a specific crc configuration/algorithm and you are unsure what are the specific parameters
of it, a look into this [crc-catalogue](http://reveng.sourceforge.net/crc-catalogue/all.htm) might help.


## Requirements
* [\>= Python 3.7](https://www.python.org)

## Installation

```shell
pip install crc
```

## Examples

### Create a Calculator

#### Pre defined configuration

```python
from crc import Calculator, Crc8

calculator = Calculator(Crc8.CCITT)
```
#### Custom configuration

```python
from crc import Calculator, Configuration

config = Configuration(
    width=8,
    poly=0x07,
    init_value=0x00,
    final_xor_value=0x00,
    reverse_input=False,
    reverse_output=False,
)

calculator = Calculator(config)
```

### Calculate a checksum

#### Standard

```python
from crc import Calculator, Crc8

expected = 0xBC
data = bytes([0, 1, 2, 3, 4, 5])
calculator = Calculator(Crc8.CCITT)

assert expected == calculator.checksum(data)
```

#### Optimized for speed

```python
from crc import Calculator, Crc8

expected = 0xBC
data = bytes([0, 1, 2, 3, 4, 5])
calculator = Calculator(Crc8.CCITT, optimized=True)

assert expected == calculator.checksum(data)
```

### Verify a checksum

#### Standard

```python
from crc import Calculator, Crc8

expected = 0xBC
data = bytes([0, 1, 2, 3, 4, 5])
calculator = Calculator(Crc8.CCITT)

assert calculator.verify(data, expected)
```

#### Optimized for speed

```python
from crc import Calculator, Crc8

expected = 0xBC
data = bytes([0, 1, 2, 3, 4, 5])
calculator = Calculator(Crc8.CCITT, optimized=True)

assert calculator.verify(data, expected)
```

### Calculate a checksum with raw registers

#### Register

```python
from crc import Crc8, Register

expected = 0xBC
data = bytes([0, 1, 2, 3, 4, 5])
register = Register(Crc8.CCITT)

register.init()
register.update(data)
assert expected == register.digest()
```
#### TableBasedRegister

```python
from crc import Crc8, TableBasedRegister

expected = 0xBC
data = bytes([0, 1, 2, 3, 4, 5])
register = TableBasedRegister(Crc8.CCITT)

register.init()
register.update(data)
assert expected == register.digest()
```

References & Resources
-----------------------
* [A Painless guide to crc error detection algorithms](http://www.zlib.net/crc_v3.txt)
* [CRC-Catalogue](http://reveng.sourceforge.net/crc-catalogue/all.htm)

