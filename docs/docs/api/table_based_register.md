---
icon: material/table-large
---

# TableBasedRegister

A CRC register which uses a precomputed lookup table. It trades a bit of memory
and setup time for significantly faster checksum calculation compared to
[`Register`](register.md).

```python
from crc import Crc8, TableBasedRegister

register = TableBasedRegister(Crc8.CCITT)

register.init()
register.update(bytes([0, 1, 2, 3, 4, 5]))
assert register.digest() == 0xBC
```

!!! tip

    Building the lookup table happens once per register, so create the register
    once and reuse it. See [raw registers](../usage/registers.md) for a guide.

::: crc.TableBasedRegister
