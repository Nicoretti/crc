---
icon: material/tune-variant
---

# Configuration

A `Configuration` describes all parameters of a CRC algorithm.

## Predefined configurations

The library ships with a large set of ready to use configurations, grouped by
width in the enums `Crc8`, `Crc16`, `Crc32` and `Crc64`. Every member is a
`Configuration` and can be passed directly to a
[`Calculator`](calculator.md):

```python
from crc import Calculator, Crc8

calculator = Calculator(Crc8.CCITT)
```

[:octicons-arrow-right-24: Browse all supported configurations](../configurations.md){ .md-button }

!!! tip "Looking for a guide?"

    This page is the API reference. For a task oriented introduction see
    [configurations](../usage/configurations.md).

## Custom configurations

Use `Configuration` directly to define an algorithm which is not part of the
predefined ones:

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

!!! warning "Supported widths"

    This library currently only supports bit widths which are a multiple of a
    full byte: 8, 16, 24, 32, ...

## Reference

::: crc.Configuration
    options:
        members: ["width", "polynomial", "init_value", "final_xor_value", "reverse_input", "reverse_output"]
