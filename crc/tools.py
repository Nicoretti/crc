#!/usr/bin/env python3
#
# Copyright (c) 2018, Nicola Coretti
# All rights reserved.
import sys
import docopt
import pkg_resources
from functools import reduce
from collections import defaultdict
if __name__ == '__main__':
    from crc import create_lookup_table
else:
    from crc.crc import create_lookup_table

EXTENSION_POINT = 'crc.cli.command'


def load_extensions():
    commands_names = [e.name for e in pkg_resources.iter_entry_points(group=EXTENSION_POINT)]
    commands = dict()
    help_template = '      {{:<{}}}       {{}}'.format(reduce(max, map(len, commands_names), 0))
    for extension in pkg_resources.iter_entry_points(group=EXTENSION_POINT):
        try:
            command = extension.load()
            command.name = extension.name
            command.info = command.__doc__.splitlines()[1].split('-')[1].strip()
            command.short_help = help_template.format(command.name, command.info)
            commands[command.name] = command
        except IndexError as ex:
            error_msg = 'Failed to load extension: {}, details {}'
            error_msg = error_msg.format(extension.name, ex)
            print(error_msg, file=sys.stderr)
    return commands


def main():
    """
    A set of crc checksum related command line tools.

    usage:
        crc [--version][--help] <command> [<args>...]

    options:

        -h, --help      prints this help dialoge
        --version       version

    commands:
    """
    def command_not_avialable(args=None):
        usage = docopt.printable_usage(main.__doc__)
        print(usage, file=sys.stderr)
        exit(-1)
    commands = load_extensions()
    for command in commands.values():
        main.__doc__ = main.__doc__.strip() + '\n' + command.short_help
    args = docopt.docopt(doc=main.__doc__, options_first=True, version='0.2.0')
    commands = defaultdict(lambda args=None: command_not_avialable, commands)
    argv = [args['<command>']] + args['<args>']
    commands[args['<command>']](argv)


def table(argv):
    """
    table - create crc lookup tables

    usage:
        crc table [options] <width> <polynom>

    arguments:
        <polynom>       hex value of the polynom used for calculating the crc table.

    options:
        -h, --help
        --version
    """
    args = docopt.docopt(doc=table.__doc__, argv=argv, version='0.1.0')
    width = int(args['<width>'])
    polynom = int(args['<polynom>'], 16)
    lookup_table = create_lookup_table(width, polynom)
    fmt_spec = '{{:0<0{}X}}'.format(width // 4)
    template = "0x{} ".format(fmt_spec)
    for id, entry in enumerate(lookup_table):
        if (id != 0) and (id % 8 == 0): print()
        print(template.format(entry), end='')
    print()
    exit(0)


def calculate(argv):
    """
    calculate - crc checksum(s)

    usage:
      crc calculate [options]

    options:
        -a, --algorithm         crc settings algorithm to use e.g. CRC8 or CRC16-CCITT
        -c, --config            a file containing a crc config
        -i, --input-file        input file
        -l, --list-algorithms   lists all supported crc algorithms
        -o, --output-file       input file [default: inpputfile.crc]
        -h, --help
        --version
    """
    args = docopt.docopt(doc=calculate.__doc__, argv=argv, version='0.1.0')
    raise NotImplementedError("Command not supported yet")


def verify(argv):
    """
    verify - crc checksum(s).

    usage:
        crc verify [options]

    options:
        -i, --input-file        nput file whose crc shall be verified
        -s, --settings-file     input file [default: inputfile.crc]
    """
    args = docopt.docopt(doc=verify.__doc__, argv=argv, version='0.1.0')
    raise NotImplementedError("Command not supported yet")


if __name__ == '__main__':
    main()
