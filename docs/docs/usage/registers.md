---
icon: material/memory
---

# Raw registers

For full control over the calculation you can drive the CRC registers yourself,
instead of going through a [`Calculator`](calculator.md). This is useful when
you want to feed data incrementally and inspect or reset the register in
between.

!!! tip "Prefer the calculator"

    For most use cases the [`Calculator`](calculator.md) is the more convenient
    choice — it wraps exactly these registers for you.

## Which register to use

| | [`Register`][crc.Register] | [`TableBasedRegister`][crc.TableBasedRegister] |
|---|---|---|
| Approach | Bit by bit | Precomputed lookup table |
| Setup cost | None | Builds a lookup table |
| Speed | Slower | Significantly faster |
| Equivalent calculator | `Calculator(config)` | `Calculator(config, optimized=True)` |

## Usage

Every register follows the same three step protocol: `init()`, `update()` and
`digest()`.

=== "Register"

    ```python
    from crc import Crc8, Register

    expected = 0xBC
    data = bytes([0, 1, 2, 3, 4, 5])
    register = Register(Crc8.CCITT)

    register.init()      # (1)!
    register.update(data)  # (2)!
    assert expected == register.digest()  # (3)!
    ```

    1. Initializes the register with the configuration's `init_value`.
    2. Feeds data into the register, can be called multiple times.
    3. Applies the final XOR value and returns the checksum.

=== "TableBasedRegister"

    ```python
    from crc import Crc8, TableBasedRegister

    expected = 0xBC
    data = bytes([0, 1, 2, 3, 4, 5])
    register = TableBasedRegister(Crc8.CCITT)

    register.init()
    register.update(data)
    assert expected == register.digest()
    ```

## Incremental updates

Because `update` can be called repeatedly, data can be processed in chunks:

```python
from crc import Crc8, Register

register = Register(Crc8.CCITT)

register.init()
for chunk in (b"12", b"34", b"56", b"78", b"9"):
    register.update(chunk)

assert register.digest() == 0xF4
```

!!! note "Reusing a register"

    Call `init()` again to reset the register before starting a new
    calculation.

## Custom registers

Both registers derive from [`BasicRegister`](../api/basic_register.md), which in turn
implements the [`AbstractRegister`](../api/abstract_register.md) interface. Implement
`AbstractRegister` if you want to provide your own register.

```
AbstractRegister
└── BasicRegister
    ├── Register
    └── TableBasedRegister
```

## Next steps

- [Calculating checksums](calculator.md) — the convenient high level API
- [`Register` API reference](../api/register.md)
- [`TableBasedRegister` API reference](../api/table_based_register.md)
