---
icon: material/memory
---

# BasicRegister

Base class which implements the parts shared by all registers, such as
initialization and the handling of the final XOR value. It leaves the actual
per byte update to its subclasses, [`Register`](register.md) and
[`TableBasedRegister`](table_based_register.md).

::: crc.BasicRegister
