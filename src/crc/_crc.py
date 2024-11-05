# Copyright (c) 2018, Nicola Coretti
# All rights reserved.

from __future__ import annotations

import abc
import argparse
import enum
import functools
import numbers
import sys
from dataclasses import dataclass
from typing import (
    BinaryIO,
    Final,
    Iterable,
    Iterator,
    Union,
)

__author__ = [
    "Nicola Coretti <nico.coretti@gmail.com>",
    "Gert van Dijk <github@gertvandijk.nl>",
]

InputType = Union[
    int,
    bytes,
    bytearray,
    memoryview,
    BinaryIO,
    Iterable[Union[bytes, bytearray, memoryview]],
]
"""Type alias for acceptable input types for [Calculator][crc.Calculator]."""


class Byte(numbers.Number):
    BIT_LENGTH: Final[int] = 8
    BIT_MASK: Final[int] = 0xFF
    _value: int

    def __init__(self, value: int = 0x00) -> None:
        self._value = value & Byte.BIT_MASK

    def __add__(self, other: Byte) -> Byte:
        if not isinstance(other, Byte):
            other = Byte(other)
        return Byte(self.value + other.value)

    def __radd__(self, other: Byte) -> Byte:
        return self + other

    def __iadd__(self, other: Byte) -> Byte:
        result = self + other
        self.value = result.value
        return self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Byte):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __len__(self) -> int:
        return Byte.BIT_LENGTH

    def __getitem__(self, index: int) -> int:
        if index >= Byte.BIT_LENGTH or index < 0:
            raise IndexError
        return (self.value & (1 << index)) >> index

    def __iter__(self) -> Iterator[int]:
        return (self[i] for i in range(len(self)))

    def __int__(self) -> int:
        return self.value

    @property
    def value(self) -> int:
        return self._value & Byte.BIT_MASK

    @value.setter
    def value(self, value: int) -> None:
        self._value = value & Byte.BIT_MASK

    def reversed(self) -> Byte:
        value = 0
        for index, bit in enumerate(reversed(self)):
            value += bit << index
        return Byte(value)


class AbstractRegister(metaclass=abc.ABCMeta):
    """
    Abstract base class / Interface a crc register needs to implement.

    Workflow:
        1. The Crc-Register needs to be initialized.    1 time     (init)
        2. Data is feed into the crc register.          1..n times (update)
        3. Final result is calculated.                  1 time     (digest)
    """

    @abc.abstractmethod
    def init(self) -> None:
        """
        Initializes the crc register.
        """

    @abc.abstractmethod
    def update(self, data: bytes) -> int:
        """
        Feeds data into the register.

        Args:
            data: which will be feed into the register.

        Returns:
            Register content after the update.
        """

    @abc.abstractmethod
    def digest(self) -> int:
        """
        Final crc checksum will be calculated.

        Returns:
            Final crc result/value (applies pending operations like final xor).
        """

    @abc.abstractmethod
    def reverse(self) -> int:
        """
        Calculates the reversed value of the crc register.

        Returns:
            The reversed value of the crc register.
        """


@dataclass(frozen=True)
class Configuration:
    """
    A Configuration provides all settings necessary to determine the concrete
    implementation of a specific crc algorithm/register.

    Example:
        Create a custom configuration

        ```python
        from crc import Configuration

        saej1850 = Configuration(
            width=8,
            polynomial=0x1D,
            init_value=0xFF,
            final_xor_value=0xFF,
            reverse_input=False,
            reverse_output=False
        )
        ```
    """

    width: int
    polynomial: int
    init_value: int = 0
    final_xor_value: int = 0
    reverse_input: bool = False
    reverse_output: bool = False


class BasicRegister(AbstractRegister):
    """
    Implements the common crc algorithm, assuming a user of this base class will provide
    an overwrite for the _process_byte method.
    """

    _topbit: int
    _bitmask: int
    _config: Configuration
    _register: int

    def __init__(self, configuration: Configuration) -> None:
        """
        Create a new BasicRegister.

        Args:
            configuration: Used to configure the crc algorithm.
        """
        if isinstance(configuration, enum.Enum):
            configuration = configuration.value
        self._topbit = 1 << (configuration.width - 1)
        self._bitmask = int(2**configuration.width - 1)
        self._config = configuration
        self._register = configuration.init_value & self._bitmask

    def __len__(self) -> int:
        """
        Returns:
            The width of the register.
        """
        return self._config.width // 8

    def __getitem__(self, index: int) -> int:
        """
        Gets a single byte of the register.

        Args:
            index: byte which shall be returned.

        Returns:
            The byte at the specified index.

        Raises:
            IndexError: Invalid index for this register.
        """
        if index >= (self._config.width / 8) or index < 0:
            raise IndexError
        shift_offset = index * 8
        return (self.register & (0xFF << shift_offset)) >> shift_offset

    def init(self) -> None:
        """
        See `AbstractRegister.init`
        """
        self.register = self._config.init_value

    def update(self, data: bytes) -> int:
        """
        See `AbstractRegister.update`
        """
        for byte in (Byte(b) for b in data):
            if self._config.reverse_input:
                byte = byte.reversed()
            self._register = self._process_byte(byte)
        return self.register

    @abc.abstractmethod
    def _process_byte(self, byte: Byte) -> int:
        """
        Feed a byte into the crc register.

        Args:
            byte: the byte which shall be processed by the crc register.

        Returns:
            The value/state the crc register needs to be put in after this byte has been
            processed.
        """

    def digest(self) -> int:
        """
        See `AbstractRegister.digest`
        """
        value = self.reverse() if self._config.reverse_output else self.register
        return value ^ self._config.final_xor_value

    def reverse(self) -> int:
        """
        See `AbstractRegister.digest`
        """
        index = 0
        reversed_value = 0
        for byte in reversed(self):
            reversed_value += int(Byte(byte).reversed()) << index
            index += 8
        return reversed_value

    def _is_division_possible(self) -> bool:
        return (self.register & self._topbit) > 0

    @property
    def register(self) -> int:
        return self._register & self._bitmask

    @register.setter
    def register(self, value: int) -> None:
        self._register = value & self._bitmask


class Register(BasicRegister):
    """
    Simple crc register, which will process one bit at the time.

    Note:
        If performance is an important issue for the crc calculation use a table based
        register.
    """

    def _process_byte(self, byte: Byte) -> int:
        """
        See BasicRegister._process_byte
        """
        self.register ^= int(byte) << (self._config.width - 8)
        for _ in byte:
            if self._is_division_possible():
                self.register = (self.register << 1) ^ self._config.polynomial
            else:
                self.register <<= 1
        return self.register


class TableBasedRegister(BasicRegister):
    """
    Lookup table based crc register.

    Info:
        This register type will be much faster than a simple bit by bit based crc
        register like `Register`.
    """

    def __init__(self, configuration: Configuration) -> None:
        """
        Creates a new table based crc register.

        Args:
            configuration: used for the crc algorithm.

        Attention:
            Creating a table based register initially might take some extra time,
            due to the fact that some lookup tables need to be calculated/initialized.
        """
        super().__init__(configuration)
        if isinstance(configuration, enum.Enum):
            configuration = configuration.value
        self._lookup_table = create_lookup_table(
            configuration.width, configuration.polynomial
        )

    def _process_byte(self, byte: Byte) -> int:
        """
        See BasicRegister._process_byte
        """
        index = int(byte) ^ (self.register >> (self._config.width - 8))
        self.register = self._lookup_table[index] ^ (self.register << 8)
        return self.register


@functools.lru_cache
def create_lookup_table(width: int, polynomial: int) -> list[int]:
    """
    Creates a crc lookup table.

    Args:
        width: of the crc checksum.
        polynomial: which is used for the crc calculation.

    Returns:
        The lookup table for the specified width and polynomial.
    """
    config = Configuration(width=width, polynomial=polynomial)
    crc_register = Register(config)
    lookup_table: list[int] = []
    for index in range(256):
        crc_register.init()
        data = bytes(index.to_bytes(1, byteorder="big"))
        crc_register.update(data)
        lookup_table.append(crc_register.digest())
    return lookup_table


class Calculator:
    def __init__(self, configuration: Configuration, optimized: bool = False) -> None:
        """
        Creates a new Calculator.

        Args:
            configuration: for the crc algorithm.
            optimized: whether a register optimized for speed shall be used.

        :warning: initializing an optimized calculator might take some extra time,
                  calculation itself will be faster though.
        """
        _types = {
            False: Register,
            True: TableBasedRegister,
        }
        klass = _types[optimized]
        self._crc_register = klass(configuration)

    def checksum(self, data: InputType) -> int:
        """
        Calculates the checksum for the given data.

        Args:
            data: which will be used as input for the checksum.

        Returns:
            Checksum for the given input data.
        """
        self._crc_register.init()
        for chunk in _bytes_generator(data):
            self._crc_register.update(chunk)
        return self._crc_register.digest()

    def verify(self, data: InputType, expected: int) -> bool:
        """
        Verifies that the checksum for the given data is the expected one.

        Args:
            data: which will be used as input for the checksum.
            expected: checksum.

        Returns:
            True if the expected checksum matches the actual checksum for the given
                data, False otherwise.
        """
        return self.checksum(data) == expected


def _bytes_generator(data: InputType) -> Iterable[bytes]:
    if isinstance(data, int):
        yield data.to_bytes(1, "big")
    elif isinstance(data, bytes):
        yield data
    elif isinstance(data, (bytearray, memoryview)):
        yield bytes(data)
    elif isinstance(data, (Iterable, BinaryIO)):
        yield from (bytes(e) for e in data)
    else:
        raise TypeError(f"Unsupported parameter type: {type(data)}")


@enum.unique
class Crc8(enum.Enum):
    CCITT = Configuration(
        width=8,
        polynomial=0x07,
        init_value=0x00,
        final_xor_value=0x00,
        reverse_input=False,
        reverse_output=False,
    )

    SAEJ1850 = Configuration(
        width=8,
        polynomial=0x1D,
        init_value=0xFF,
        final_xor_value=0xFF,
        reverse_input=False,
        reverse_output=False,
    )

    SAEJ1850_ZERO = Configuration(
        width=8,
        polynomial=0x1D,
        init_value=0x00,
        final_xor_value=0x00,
        reverse_input=False,
        reverse_output=False,
    )

    AUTOSAR = Configuration(
        width=8,
        polynomial=0x2F,
        init_value=0xFF,
        final_xor_value=0xFF,
        reverse_input=False,
        reverse_output=False,
    )

    BLUETOOTH = Configuration(
        width=8,
        polynomial=0xA7,
        init_value=0x00,
        final_xor_value=0x00,
        reverse_input=True,
        reverse_output=True,
    )

    MAXIM_DOW = Configuration(
        width=8,
        polynomial=0x31,
        init_value=0,
        final_xor_value=0,
        reverse_input=True,
        reverse_output=True,
    )

    ITU = Configuration(
        width=8,
        polynomial=0x07,
        init_value=0x00,
        final_xor_value=0x55,
        reverse_input=False,
        reverse_output=False,
    )

    ROHC = Configuration(
        width=8,
        polynomial=0x07,
        init_value=0xFF,
        final_xor_value=0x00,
        reverse_input=True,
        reverse_output=True,
    )


@enum.unique
class Crc16(enum.Enum):
    XMODEM = Configuration(
        width=16,
        polynomial=0x1021,
        init_value=0x0000,
        final_xor_value=0x0000,
        reverse_input=False,
        reverse_output=False,
    )

    GSM = Configuration(
        width=16,
        polynomial=0x1021,
        init_value=0x0000,
        final_xor_value=0xFFFF,
        reverse_input=False,
        reverse_output=False,
    )

    PROFIBUS = Configuration(
        width=16,
        polynomial=0x1DCF,
        init_value=0xFFFF,
        final_xor_value=0xFFFF,
        reverse_input=False,
        reverse_output=False,
    )

    MODBUS = Configuration(
        width=16,
        polynomial=0x8005,
        init_value=0xFFFF,
        final_xor_value=0x0000,
        reverse_input=True,
        reverse_output=True,
    )

    IBM_3740 = Configuration(
        width=16,
        polynomial=0x1021,
        init_value=0xFFFF,
        final_xor_value=0x0000,
        reverse_input=False,
        reverse_output=False,
    )

    KERMIT = Configuration(
        width=16,
        polynomial=0x1021,
        init_value=0x0000,
        final_xor_value=0x0000,
        reverse_input=True,
        reverse_output=True,
    )

    IBM = Configuration(
        width=16,
        polynomial=0x8005,
        init_value=0x0000,
        final_xor_value=0x0000,
        reverse_input=True,
        reverse_output=True,
    )

    MAXIM = Configuration(
        width=16,
        polynomial=0x8005,
        init_value=0x0000,
        final_xor_value=0xFFFF,
        reverse_input=True,
        reverse_output=True,
    )

    USB = Configuration(
        width=16,
        polynomial=0x8005,
        init_value=0xFFFF,
        final_xor_value=0xFFFF,
        reverse_input=True,
        reverse_output=True,
    )

    X25 = Configuration(
        width=16,
        polynomial=0x1021,
        init_value=0xFFFF,
        final_xor_value=0xFFFF,
        reverse_input=True,
        reverse_output=True,
    )

    DNP = Configuration(
        width=16,
        polynomial=0x3D65,
        init_value=0x0000,
        final_xor_value=0xFFFF,
        reverse_input=True,
        reverse_output=True,
    )


@enum.unique
class Crc32(enum.Enum):
    CRC32 = Configuration(
        width=32,
        polynomial=0x04C11DB7,
        init_value=0xFFFFFFFF,
        final_xor_value=0xFFFFFFFF,
        reverse_input=True,
        reverse_output=True,
    )

    AUTOSAR = Configuration(
        width=32,
        polynomial=0xF4ACFB13,
        init_value=0xFFFFFFFF,
        final_xor_value=0xFFFFFFFF,
        reverse_input=True,
        reverse_output=True,
    )

    BZIP2 = Configuration(
        width=32,
        polynomial=0x04C11DB7,
        init_value=0xFFFFFFFF,
        final_xor_value=0xFFFFFFFF,
        reverse_input=False,
        reverse_output=False,
    )

    POSIX = Configuration(
        width=32,
        polynomial=0x04C11DB7,
        init_value=0x00000000,
        final_xor_value=0xFFFFFFFF,
        reverse_input=False,
        reverse_output=False,
    )


@enum.unique
class Crc64(enum.Enum):
    CRC64 = Configuration(
        width=64,
        polynomial=0x42F0E1EBA9EA3693,
        init_value=0x0000000000000000,
        final_xor_value=0x0000000000000000,
        reverse_input=False,
        reverse_output=False,
    )


def _argument_parser() -> argparse.ArgumentParser:
    into_int = functools.partial(int, base=0)
    program = "crc"
    description = "A set of crc checksum related command line tools."
    parser = argparse.ArgumentParser(
        prog=program,
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparsers = parser.add_subparsers()

    table_command = subparsers.add_parser(
        "table", help="Generates lookup tables for various crc algorithm settings"
    )
    table_command.add_argument(
        "width",
        metavar="<width>",
        type=into_int,
        help="width of the crc algorithm, common width's are 8, 16, 32, 64",
    )
    table_command.add_argument(
        "polynomial",
        metavar="<polynomial>",
        type=into_int,
        help="hex value of the polynomial used for calculating the crc table",
    )
    table_command.set_defaults(func=table)
    return parser


def _generate_template(width: int) -> str:
    return f"0x{{:0{(width + 3) // 4}X}}"


def table(args: argparse.Namespace) -> bool:
    if not (args.width and args.polynomial):
        return False
    columns = 8
    width = args.width
    polynomial = args.polynomial
    lookup_table = create_lookup_table(width, polynomial)
    template = _generate_template(width)
    rows = (lookup_table[i : i + columns] for i in range(0, len(lookup_table), columns))
    print("\n".join(" ".join(template.format(value) for value in r) for r in rows))
    return True


def main(argv: list[str] | None = None) -> None:
    parser = _argument_parser()
    args = parser.parse_args(argv)
    if "func" in args:
        exit_code = 0 if args.func(args) else -1
        sys.exit(exit_code)
    else:
        parser.print_help()
        sys.exit(-1)


# Although there's a __main__.py to invoke main(), let's keep this in for users who
# would like to use crc as a single-file.
if __name__ == "__main__":
    main()  # pragma: no cover
