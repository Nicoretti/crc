---
icon: material/calculator-variant
---

# Calculating checksums

The [`Calculator`](../api/calculator.md) combines a [configuration](../api/configuration.md) with a register implementation
and exposes two methods: `checksum` and `verify`.

## Create a calculator

=== "Predefined configuration"

    ```python
    from crc import Calculator, Crc8

    calculator = Calculator(Crc8.CCITT)
    ```

=== "Custom configuration"

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

[:octicons-arrow-right-24: More about configurations](configurations.md)

## Calculate a checksum

=== "Standard"

    ```python
    from crc import Calculator, Crc8

    expected = 0xBC
    data = bytes([0, 1, 2, 3, 4, 5])
    calculator = Calculator(Crc8.CCITT)

    assert expected == calculator.checksum(data)
    ```

=== "Optimized for speed"

    ```python hl_lines="5"
    from crc import Calculator, Crc8

    expected = 0xBC
    data = bytes([0, 1, 2, 3, 4, 5])
    calculator = Calculator(Crc8.CCITT, optimized=True)  # (1)!

    assert expected == calculator.checksum(data)
    ```

    1. Builds a lookup table upfront, which trades a bit of memory and setup
       time for significantly faster checksum calculation.

## Verify a checksum

=== "Standard"

    ```python
    from crc import Calculator, Crc8

    expected = 0xBC
    data = bytes([0, 1, 2, 3, 4, 5])
    calculator = Calculator(Crc8.CCITT)

    assert calculator.verify(data, expected)
    ```

=== "Optimized for speed"

    ```python hl_lines="5"
    from crc import Calculator, Crc8

    expected = 0xBC
    data = bytes([0, 1, 2, 3, 4, 5])
    calculator = Calculator(Crc8.CCITT, optimized=True)

    assert calculator.verify(data, expected)
    ```

## Standard vs. optimized

| | Standard | Optimized |
|---|---|---|
| Created with | `Calculator(config)` | `Calculator(config, optimized=True)` |
| Register used | [`Register`][crc.Register] | [`TableBasedRegister`][crc.TableBasedRegister] |
| Setup cost | None | Builds a lookup table |
| Calculation speed | Slower | Significantly faster |
| Best for | One off checksums | Lots of data, repeated use |

!!! tip "Create it once, reuse it"

    Creating an optimized calculator builds a lookup table. Create it once and
    reuse it, rather than creating a new one for every checksum.

## Supported input types

Both `checksum` and `verify` accept a wide range of input types, see
[`InputType`][crc.InputType] for the formal definition.

=== "int"

    ```python
    from crc import Calculator, Crc8

    expected = 0x20
    data = 97
    calculator = Calculator(Crc8.CCITT, optimized=True)

    assert calculator.checksum(data) == expected
    ```

=== "bytes"

    ```python
    from crc import Calculator, Crc8

    expected = 0xF4
    data = b"123456789"
    calculator = Calculator(Crc8.CCITT, optimized=True)

    assert calculator.checksum(data) == expected
    ```

=== "bytearray"

    ```python
    from crc import Calculator, Crc8

    expected = 0xF4
    data = bytearray(b"123456789")
    calculator = Calculator(Crc8.CCITT, optimized=True)

    assert calculator.checksum(data) == expected
    ```

=== "File"

    ```python
    from crc import Calculator, Crc8

    expected = 0xF4
    calculator = Calculator(Crc8.CCITT, optimized=True)

    with open("afile.txt", "rb") as f:  # (1)!
        assert calculator.checksum(f) == expected
    ```

    1. Make sure to open the file in binary mode (`"rb"`), files are read in
       chunks, so even large files do not need to fit into memory.

=== "BytesIO"

    ```python
    import io

    from crc import Calculator, Crc8

    expected = 0xF4
    data = io.BytesIO(b"123456789")
    calculator = Calculator(Crc8.CCITT, optimized=True)

    assert calculator.checksum(data) == expected
    ```

=== "Iterable of bytes"

    ```python
    from crc import Calculator, Crc8

    expected = 0xF4
    calculator = Calculator(Crc8.CCITT, optimized=True)
    data = (data for data in [b"12", b"34", b"56", b"78", b"9"])

    assert calculator.checksum(data) == expected
    ```

=== "Byte convertibles"

    ```python
    from crc import Calculator, Crc8


    class ByteConvertible:
        def __init__(self, data):
            self._data = data

        def __bytes__(self):
            return self._data.encode("utf-8")


    expected = 0xF4
    calculator = Calculator(Crc8.CCITT, optimized=True)
    data = ByteConvertible("123456789")

    assert calculator.checksum(bytes(data)) == expected
    ```

## Next steps

- [Configurations](configurations.md) — pick or define the CRC algorithm
- [Raw registers](registers.md) — drive the calculation yourself
- [`Calculator` API reference](../api/calculator.md)
