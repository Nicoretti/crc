# CLI Tools
The crc library comes with a small command line tool which can generate crc lookup tables if needed.

```console
usage: crc table [-h] <width> <polynomial>

positional arguments:
  <width>       width of the crc algorithm, common width's are 8, 16, 32, 64
  <polynomial>  hex value of the polynomial used for calculating the crc table

optional arguments:
  -h, --help    show this help message and exit

```

Example Usage:

```
user@host ~$ crc table 8 0x7D
```