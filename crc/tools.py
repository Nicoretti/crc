#!/usr/bin/env python3
#
# Copyright (c) 2018, Nicola Coretti
# All rights reserved.
import sys
import argparse
from functools import partial
from crc.crc import create_lookup_table


def argument_parser():
    into_int = partial(int, base=0)
    prog = 'crc'
    description = 'A set of crc checksum related command line tools.'
    parser = argparse.ArgumentParser(prog=prog, description=description)
    subparsers = parser.add_subparsers()
    t = subparsers.add_parser('table')
    t.add_argument('width', metavar='<width>', type=into_int,
                   help='width of the crc algorithm, common withd\'s are 8, 16, 32, 64.')
    t.add_argument('polynom', metavar='<polynom>', type=into_int,
                   help='hex value of the polynom used for calculating the crc table.')
    t.set_defaults(func=table)
    return parser


def main(argv=None):
    parser = argument_parser()
    args = parser.parse_args(argv)
    if 'func' in args:
        exit_code = 0 if args.func(args) else -1
        sys.exit(exit_code)
    else:
        parser.print_help()
        sys.exit(-1)


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
    exit(0)


if __name__ == '__main__':
    main()
