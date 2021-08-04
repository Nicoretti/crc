#!/usr/bin/env python3
#
# Copyright (c) 2018, Nicola Coretti
# All rights reserved.

import sys
import abc
import enum
import numbers
import functools
import argparse
from dataclasses import dataclass

MAJOR_VERSION = 1
MINOR_VERSION = 0
PATCH_VERSION = 1

LIBRARY_VERSION = f'{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}'

__author__ = 'Nicola Coretti'
__email__ = 'nico.coretti@gmail.com'
__version__ = LIBRARY_VERSION


class AbstractCrcRegister(metaclass=abc.ABCMeta):
    """
    Abstract base class / Interface a crc register needs to implement.

    Workflow:
        1. The Crc-Register needs to be initialized.    1 time     (init)
        2. Data is feed into the crc register.          1..n times (update)
        3. Final result is calculated.                  1 time     (digest)
    """

    @abc.abstractmethod
    def init(self):
        """
        Initializes the crc register.
        """
        pass

    @abc.abstractmethod
    def update(self, data):
        """
        Feeds the provided data into the crc register.

        :param bytes data: a bytes like object or ann object which can be converted to a bytes
                     like object using the built in bytes() function.
        :return: the current value of the crc register.
        """
        pass

    @abc.abstractmethod
    def digest(self):
        """
        Final crc checksum will be calculated.

        :return: the final crc checksum.
        :rtype: int.
        """
        pass

    @abc.abstractmethod
    def reverse(self):
        """
        Calculates the reversed value of the crc register.

        :return: the the reversed value of the crc register.
        """
        pass


@dataclass(frozen=True)
class Configuration(object):
    """
    A Configuration provides all settings necessary to determine the concrete
    implementation of a specific crc algorithm/register.
    """
    width: int
    polynomial: int
    init_value: int = 0
    final_xor_value: int = 0
    reverse_input: bool = False
    reverse_output: bool = False


class CrcRegisterBase(AbstractCrcRegister):
    """
    Implements the common crc algorithm, assuming a user of this base
    class will provide an overwrite for the _process_byte method.
    """

    def __init__(self, configuration):
        """
        Create a new CrcRegisterBase.

        :param configuration: used for the crc algorithm.
        """
        if isinstance(configuration, enum.Enum):
            configuration = configuration.value
        self._topbit = 1 << (configuration.width - 1)
        self._bitmask = 2 ** configuration.width - 1
        self._config = configuration
        self._register = configuration.init_value & self._bitmask

    def __len__(self):
        """
        Returns the length (width) of the register.

        :return: the register size/width in bytes.
        """
        return self._config.width // 8

    def __getitem__(self, index):
        """
        Gets a single byte of the register.

        :param index: byte which shall be returned.
        :return: the byte at the specified index.
        :raises IndexError: if the index is out of bounce.
        """
        if index >= (self._config.width / 8) or index < 0:
            raise IndexError
        shift_offset = index * 8
        return (self.register & (0xFF << shift_offset)) >> shift_offset

    def init(self):
        """
        See AbstractCrcRegister.init
        """
        self.register = self._config.init_value

    def update(self, data):
        """
        See AbstractCrcRegister.update
        """
        for byte in data:
            byte = Byte(byte)
            if self._config.reverse_input:
                byte = byte.reversed()
            self._register = self._process_byte(byte)
        return self.register

    @abc.abstractmethod
    def _process_byte(self, byte):
        """
        Processes an entire byte feed to the crc register.

        :param byte: the byte which shall be processed by the crc register.
        :return: the new value of the crc register will have after the byte have been processed.
        """
        pass

    def digest(self):
        """
        See AbstractCrcRegister.digest
        """
        if self._config.reverse_output:
            self.register = self.reverse()
        return self.register ^ self._config.final_xor_value

    def reverse(self):
        """
        See AbstractCrcRegister.digest
        """
        index = 0
        reversed_value = 0
        for byte in reversed(self):
            reversed_value += int(Byte(byte).reversed()) << index
            index += 8
        return reversed_value

    def _is_division_possible(self):
        return (self.register & self._topbit) > 0

    @property
    def register(self):
        return self._register & self._bitmask

    @register.setter
    def register(self, value):
        self._register = value & self._bitmask


class CrcRegister(CrcRegisterBase):
    """
    Simple crc register, which will process one bit at the time.

    .. note:

        If performance is an important issue for the crc calculation use a table
        based register.
    """

    def __init__(self, configuration):
        super().__init__(configuration)

    def _process_byte(self, byte):
        """
        See CrcRegisterBase._process_byte
        """
        self.register ^= int(byte) << (self._config.width - 8)
        for bit in byte:
            if self._is_division_possible():
                self.register = (self.register << 1) ^ self._config.polynomial
            else:
                self.register <<= 1
        return self.register


class TableBasedCrcRegister(CrcRegisterBase):
    """
    Lookup table based crc register.

    .. note::

        this register type will be much faster than a simple bit by bit based crc register.
        (e.g. CrcRegister)
    """

    def __init__(self, configuration):
        """
        Creates a new table based crc register.

        :param configuration: used for the crc algorithm.

        :attention: creating a table based register initially might take some extra time, due to the
                    fact that some lookup tables need to be calculated/initialized .
        """
        super().__init__(configuration)
        if isinstance(configuration, enum.Enum):
            configuration = configuration.value
        self._lookup_table = create_lookup_table(configuration.width, configuration.polynomial)

    def _process_byte(self, byte):
        """
        See CrcRegisterBase._process_byte
        """
        index = int(byte) ^ (self.register >> (self._config.width - 8))
        self.register = self._lookup_table[index] ^ (self.register << 8)
        return self.register


class Byte(numbers.Number):
    BIT_LENGTH = 8
    BIT_MASK = 0xFF

    def __init__(self, value=0x00):
        self._value = value & Byte.BIT_MASK

    def __add__(self, other):
        if not isinstance(other, Byte):
            other = Byte(other)
        return Byte(self.value + other.value)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        result = self + other
        self.value = result.value
        return self

    def __eq__(self, other):
        if not isinstance(other, Byte):
            raise TypeError('unsupported operand')
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __len__(self):
        return Byte.BIT_LENGTH

    def __getitem__(self, index):
        if index >= Byte.BIT_LENGTH or index < 0:
            raise IndexError
        return (self.value & (1 << index)) >> index

    def __int__(self):
        return self.value

    @property
    def value(self):
        return self._value & Byte.BIT_MASK

    @value.setter
    def value(self, value):
        self._value = value & Byte.BIT_MASK

    def reversed(self):
        value = 0
        index = 0
        for bit in reversed(self):
            value += bit << index
            index += 1
        return Byte(value)


@functools.lru_cache()
def create_lookup_table(width, polynom):
    """
    Creates a crc lookup table.

    :param int width: of the crc checksum.
    :parma int polynom: which is used for the crc calculation.
    """
    config = Configuration(width=width, polynomial=polynom)
    crc_register = CrcRegister(config)
    lookup_table = list()
    for index in range(0, 256):
        crc_register.init()
        data = bytes((index).to_bytes(1, byteorder='big'))
        crc_register.update(data)
        lookup_table.append(crc_register.digest())
    return lookup_table


class CrcCalculator(object):

    def __init__(self, configuration, table_based=False):
        """
        Creates a new CrcCalculator.

        :param configuration: for the crc algorithm.
        :param table_based: if true a tables based register will be used for the calculations.

        :attention: initializing a table based calculator might take some extra time, due to the
                    fact that the lookup table need to be initialized.
        """
        if table_based:
            self._crc_register = TableBasedCrcRegister(configuration)
        else:
            self._crc_register = CrcRegister(configuration)

    def calculate_checksum(self, data):
        self._crc_register.init()
        self._crc_register.update(data)
        return self._crc_register.digest()

    def verify_checksum(self, data, expected_checksum):
        return self.calculate_checksum(data) == expected_checksum


@enum.unique
class Crc8(enum.Enum):
    CCITT = Configuration(
        width=8,
        polynomial=0x07,
        init_value=0x00,
        final_xor_value=0x00,
        reverse_input=False,
        reverse_output=False
    )

    SAEJ1850 = Configuration(
        width=8,
        polynomial=0x1D,
        init_value=0x00,
        final_xor_value=0x00,
        reverse_input=False,
        reverse_output=False
    )

    AUTOSAR = Configuration(
        width=8,
        polynomial=0x2F,
        init_value=0xFF,
        final_xor_value=0xFF,
        reverse_input=False,
        reverse_output=False
    )

    BLUETOOTH = Configuration(
        width=8,
        polynomial=0xA7,
        init_value=0x00,
        final_xor_value=0x00,
        reverse_input=True,
        reverse_output=True
    )


@enum.unique
class Crc16(enum.Enum):
    CCITT = Configuration(
        width=16,
        polynomial=0x1021,
        init_value=0x0000,
        final_xor_value=0x0000,
        reverse_input=False,
        reverse_output=False
    )

    GSM = Configuration(
        width=16,
        polynomial=0x1021,
        init_value=0x0000,
        final_xor_value=0xFFFF,
        reverse_input=False,
        reverse_output=False
    )

    PROFIBUS = Configuration(
        width=16,
        polynomial=0x1DCF,
        init_value=0xFFFF,
        final_xor_value=0xFFFF,
        reverse_input=False,
        reverse_output=False
    )


@enum.unique
class Crc32(enum.Enum):
    CRC32 = Configuration(
        width=32,
        polynomial=0x04C11DB7,
        init_value=0xFFFFFFFF,
        final_xor_value=0xFFFFFFFF,
        reverse_input=True,
        reverse_output=True
    )

    AUTOSAR = Configuration(
        width=32,
        polynomial=0xF4ACFB13,
        init_value=0xFFFFFFFF,
        final_xor_value=0xFFFFFFFF,
        reverse_input=True,
        reverse_output=True
    )

    BZIP2 = Configuration(
        width=32,
        polynomial=0x04C11DB7,
        init_value=0xFFFFFFFF,
        final_xor_value=0xFFFFFFFF,
        reverse_input=False,
        reverse_output=False
    )

    POSIX = Configuration(
        width=32,
        polynomial=0x04C11DB7,
        init_value=0x00000000,
        final_xor_value=0xFFFFFFFF,
        reverse_input=False,
        reverse_output=False
    )


@enum.unique
class Crc64(enum.Enum):
    CRC64 = Configuration(
        width=64,
        polynomial=0x42F0E1EBA9EA3693,
        init_value=0x0000000000000000,
        final_xor_value=0x0000000000000000,
        reverse_input=False,
        reverse_output=False
    )


CRC_TYPES = {
    Crc8.__name__: Crc8,
    Crc16.__name__: Crc16,
    Crc32.__name__: Crc32,
    Crc64.__name__: Crc64
}


def argument_parser():
    into_int = functools.partial(int, base=0)
    program = 'crc'
    description = 'A set of crc checksum related command line tools.'
    parser = argparse.ArgumentParser(prog=program, description=description,
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
    if not (args.width and args.polynom):
        return False
    width = args.width
    polynom = args.polynom
    lookup_table = create_lookup_table(width, polynom)
    fmt_spec = '{{:0<0{}X}}'.format(width // 4)
    template = "0x{} ".format(fmt_spec)
    for id, entry in enumerate(lookup_table):
        if (id != 0) and (id % 8 == 0):
            print()
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
