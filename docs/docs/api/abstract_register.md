---
icon: material/vector-square
---

# AbstractRegister

Interface all CRC registers implement. Implement it if you want to provide your
own register, otherwise use [`Register`](register.md) or
[`TableBasedRegister`](table_based_register.md).

!!! info "Register hierarchy"

    ```
    AbstractRegister
    └── BasicRegister
        ├── Register
        └── TableBasedRegister
    ```

::: crc.AbstractRegister
