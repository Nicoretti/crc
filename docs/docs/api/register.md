---
icon: material/memory
---

# Register

A straightforward, bit by bit CRC register. Use it when you need full control
over the calculation, e.g. to process data incrementally.

```python
from crc import Crc8, Register

register = Register(Crc8.CCITT)

register.init()
register.update(bytes([0, 1, 2, 3, 4, 5]))
assert register.digest() == 0xBC
```

!!! tip

    For most use cases the [`Calculator`](calculator.md) is the more convenient
    choice. If you need speed, use [`TableBasedRegister`](table_based_register.md).
    See [raw registers](../usage/registers.md) for a guide.

::: crc.Register
