---
icon: material/tune-variant
---

# Configurations

A configuration describes all parameters of a CRC algorithm. You either pick
one of the predefined configurations, or define your own.

## Predefined configurations

The library ships with a wide range of commonly used configurations, grouped by
width in the enums `Crc8`, `Crc16`, `Crc32` and `Crc64`:

| CRC8            | CRC16      | CRC32     | CRC64   |
|-----------------|------------|-----------|---------|
| `CCITT`         | `XMODEM`   | `CRC32`   | `CRC64` |
| `AUTOSAR`       | `GSM`      | `AUTOSAR` |         |
| `SAEJ1850`      | `PROFIBUS` | `BZIP2`   |         |
| `SAEJ1850_ZERO` | `MODBUS`   | `POSIX`   |         |
| `BLUETOOTH`     | `IBM_3740` |           |         |
| `MAXIM_DOW`     | `KERMIT`   |           |         |

Every member is a ready to use [`Configuration`](../api/configuration.md):

```python
from crc import Calculator, Crc16

calculator = Calculator(Crc16.MODBUS)
```

[:octicons-arrow-right-24: Browse all configurations and their parameters](../configurations.md){ .md-button }


## Custom configurations

To define a custom configuration you need to know the following parameters:

| Parameter          | Description                                          |
|--------------------|------------------------------------------------------|
| `width`            | Width of the CRC in bits, e.g. `8`, `16`, `32`, `64` |
| `polynomial`       | Generator polynomial of the algorithm                |
| `init_value`       | Value the register is initialized with               |
| `final_xor_value`  | Value the final register is XOR'ed with              |
| `reverse_input`    | Whether the input bytes are reflected                |
| `reverse_output`   | Whether the final register is reflected              |

```python
from crc import Calculator, Configuration

config = Configuration(
    width=8,
    polynomial=0x07,
    init_value=0x00,
    final_xor_value=0x00,
    reverse_input=False,
    reverse_output=False,
)

calculator = Calculator(config)
```

!!! failure "Supported widths"

    This library currently only supports bit widths which are a multiple of a
    full byte: 8, 16, 24, 32, ...

!!! question "Only know the name of the algorithm?"

    If you only know the name of a CRC algorithm and are unsure about its
    parameters, the [:material-note-search: CRC catalogue](http://reveng.sourceforge.net/crc-catalogue/all.htm)
    is a great place to look them up.

## Next steps

- [Calculating checksums](calculator.md) — use a configuration with a calculator
- [`Configuration` API reference](../api/configuration.md)
