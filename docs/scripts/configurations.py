from inspect import cleandoc
from io import StringIO

import mkdocs_gen_files

from crc import (
    Crc8,
    Crc16,
    Crc32,
    Crc64,
)

_TAB_META_TEMPLATE = cleandoc(
    """
=== "{{name}}"

    <div class="grid cards" markdown>

     - *Width:* **{{width}}**
     - *Final Xor:* **0x{{final_xor:0{length}X}}**
     - *Init Value:* **0x{{init_value:0{length}X}}**
     - *Rev Input:* **{{reverse_input}}**
     - *Polynomial:* **0x{{polynomial:0{length}X}}**
     - *Rev Output:* **{{reverse_output}}**

    </div>
"""
)


def as_content_tabs(config_group):
    output = StringIO()
    print(f"## {config_group.__name__} ", file=output)
    group2length = {Crc8: 2, Crc16: 4, Crc32: 8, Crc64: 16}
    for cfg in config_group:
        length = group2length[type(cfg)]
        tab_template = _TAB_META_TEMPLATE.format(length=length)
        row = tab_template.format(
            name=cfg.name,
            width=cfg.value.width,
            polynomial=cfg.value.polynomial,
            init_value=cfg.value.init_value,
            final_xor=cfg.value.final_xor_value,
            reverse_input=cfg.value.reverse_input,
            reverse_output=cfg.value.reverse_output,
        )
        print(row, file=output)

    return output.getvalue()


def main():
    filename = "configurations.md"
    with mkdocs_gen_files.open(filename, "w") as f:
        config_groups = (Crc8, Crc16, Crc32, Crc64)
        for group in config_groups:
            t = as_content_tabs(config_group=group)
            print(t, file=f)


main()
