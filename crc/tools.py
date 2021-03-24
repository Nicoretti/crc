#!/usr/bin/env python3
#
# Copyright (c) 2018, Nicola Coretti
# All rights reserved.
import sys
import argparse
from functools import partial
from crc.crc import create_lookup_table, Crc8, Crc16, Crc32, Crc64, CrcCalculator

CRC_TYPES = {
    Crc8.__name__: Crc8,
    Crc16.__name__: Crc16,
    Crc32.__name__: Crc32,
    Crc64.__name__: Crc64
}


def argument_parser():
    into_int = partial(int, base=0)
    prog = 'crc'
    description = 'A set of crc checksum related command line tools.'
    parser = argparse.ArgumentParser(prog=prog, description=description,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers()

    t = subparsers.add_parser('table', help='Generates lookup tables for various crc algorithm settings')
    t.add_argument('width', metavar='<width>', type=into_int,
                   help='width of the crc algorithm, common width\'s are 8, 16, 32, 64')
    t.add_argument('polynom', metavar='<polynom>', type=into_int,
                   help='hex value of the polynom used for calculating the crc table')
    t.set_defaults(func=table)

    c = subparsers.add_parser('checksum', help='Calculate checksum(s) for the specified input(s)')
    c.add_argument('inputs', nargs='*', type=argparse.FileType('r'), default=[sys.stdin],
                   help='who will be feed into the crc calculation')
    c.add_argument('-c', '--category', choices=[t for t in CRC_TYPES], default=Crc8.__name__,
                   help='of crc algorithms which shall be used for calculation')
    c.set_defaults(func=checksum)

    return parser


def table(args):
    width = args.width
    polynom = args.polynom
    lookup_table = create_lookup_table(width, polynom)
    fmt_spec = '{{:0<0{}X}}'.format(width // 4)
    template = "0x{} ".format(fmt_spec)
    for id, entry in enumerate(lookup_table):
        if (id != 0) and (id % 8 == 0): print()
        print(template.format(entry), end='')
    print()
    return True


def checksum(args):
    data = bytearray()
    for input in args.inputs:
        data.extend(bytes(input.read(), 'utf-8'))
    category = CRC_TYPES[args.category]
    for algorithm in sorted(category, key=str):
        name = f'{algorithm}'.split('.')[1]
        calculator = CrcCalculator(algorithm, True)
        print(f'{name}: 0x{calculator.calculate_checksum(data):X}')
    return True


def main(argv=None):
    parser = argument_parser()
    args = parser.parse_args(argv)
    if 'func' in args:
        exit_code = 0 if args.func(args) else -1
        sys.exit(exit_code)
    else:
        parser.print_help()
        sys.exit(-1)


if __name__ == '__main__':
    main()
