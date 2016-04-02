import abc
import enum
import numbers
from array import array

MAJOR_VERSION = 1
MINOR_VERSION = 0
PATCH_VERSION = 0

VERSION_TEMPLATE = '{major}.{minor}.{patch}'
LIBRARY_VERSION = VERSION_TEMPLATE.format(major=MAJOR_VERSION, minor=MINOR_VERSION, patch=PATCH_VERSION)

__author__ = 'Nicola Coretti'
__email__ = 'nico.coretti@gmail.com'
__version__ = LIBRARY_VERSION


class Byte(numbers.Number):

    def __init__(self, value=0x00):
        self._bitmask = 0xFF
        self._bit_length = 8
        self._value = value & self._bitmask

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
        return self._bit_length

    def __getitem__(self, item):
        if item >= self._bit_length or item < 0:
            raise IndexError
        return (self.value & (1 << item)) >> item

    def __int__(self):
        return self.value

    @property
    def value(self):
        return self._value & self._bitmask

    @value.setter
    def value(self, value):
        self._value = value & self._bitmask

    def reversed(self):
        value = 0
        index = 0
        for bit in reversed(self):
            value += bit << index
            index += 1
        return Byte(value)


class Configuration(object):
    """
    A Configuration provides all settings necessary to determine the concrete
    implementation of a specific crc algorithm/register.
    """

    def __init__(self, width, polynom, init_value=0, final_xor_value=0, reverse_input=False, reverse_output=False):
        self._width = width
        self._polynom = polynom
        self._init_value = init_value
        self._final_xor_value = final_xor_value
        self._reverse_input = reverse_input
        self._reverse_output = reverse_output

    @property
    def width(self):
        return self._width

    @property
    def polynom(self):
        return self._polynom

    @property
    def init_value(self):
        return self._init_value

    @property
    def final_xor_value(self):
        return self._final_xor_value

    @property
    def reverse_input(self):
        return self._reverse_input

    @property
    def reverse_output(self):
        return self._reverse_output


@enum.unique
class Crc8(enum.Enum):
    CCITT = Configuration(8, 0x07, 0, 0, False, False)
    SAEJ1850 = Configuration(8, 0x1D, 0, 0, False, False)


@enum.unique
class Crc16(enum.Enum):
    CCITT = Configuration(16, 0x1021, False, False)


@enum.unique
class Crc32(enum.Enum):
    pass


def is_crc_configruation(configuration):
    """
    Checks whether or not a specified configuration is a crc configuration or not.

    :param configuration: which will be checked.

    :return: True if it is a valid crc configuration, otherwise False.
    """
    return isinstance(configuration, Configuration) \
           or isinstance(configuration, Crc8) \
           or isinstance(configuration, Crc16) \
           or isinstance(configuration, Crc32)


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


class CrcRegisterBase(AbstractCrcRegister):
    """
    Already implements commonly used methods, but still is an abstract class.

    Subclasses need to implement the update method an comply to the following contract:
    - tbd ...
    """

    def __init__(self, configuration):
        if not is_crc_configruation(configuration):
            raise Exception("No valid crc configuration provided")
        if isinstance(configuration, enum.Enum):
            configuration = configuration.value
        self._topbit = 1 << (configuration.width - 1)
        self._bitmask = 2 ** configuration.width - 1
        self._config = configuration
        self._register = configuration.init_value & self._bitmask

    def __len__(self):
        return self._config.width // 8

    def __getitem__(self, index):
        if index >= (self._config.width / 8) or index < 0:
            raise IndexError
        shift_offset = index * 8
        return (self.register & (0xFF << shift_offset)) >> shift_offset

    def init(self):
        self.register = self._config.init_value

    def update(self, data):
        for byte in data:
            byte = Byte(byte)
            if self._config.reverse_input:
                byte = byte.reversed()
            self._register = self._process_byte(byte)
        return self.register

    @abc.abstractmethod
    def _process_byte(self, byte):
        pass

    def digest(self):
        if self._config.reverse_output:
            self.register = self.reverse()
        return self.register ^ self._config.final_xor_value

    def reverse(self):
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
    A primitive loop based crc register.

    .. note:

        If performance is an important issue for the crc calcualation use table
        based register.
    """

    def __init__(self, configuration):
        super().__init__(configuration)

    def _process_byte(self, byte):
        self.register ^= int(byte) << (self._config.width - 8)
        for bit in byte:
            if self._is_division_possible():
                self.register = (self.register << 1) ^ self._config.polynom
            else:
                self.register <<= 1
        return self.register


class TableBasedCrcRegister(CrcRegisterBase):

    def __init__(self, configuration, lookup_table):
        super().__init__(configuration)
        self._lookup_table = lookup_table

    def _process_byte(self, byte):
        index = byte ^ (self.register >> (self._config.width - 8))
        self.register = self._lookup_table[index] ^ (self.register << 8)
        return self.register


def create_lookup_table(width, polynom):
    """
    Creates a crc lookup table.

    :param int width: of the crc checksum.
    :parma int polynom: which is used for the crc calculation.
    """
    config = Configuration(width=width, polynom=polynom)
    crc_register = CrcRegister(config)
    lookup_table = list()
    for index in range(0, 256):
        crc_register.init()
        data = bytes((index).to_bytes(1, byteorder='big'))
        crc_register.update(data)
        lookup_table.append(crc_register.digest())

    return lookup_table


class CrcCalculator(object):

    def __init__(self, configuration, table_based=True):
        self._crc_register = CrcRegister(configuration)

    def calculate_checksum(self, data):
        self._crc_register.init()
        self._crc_register.update(data)
        return self._crc_register.digest()


LOOKUP_TABLES = {
    Crc8: {
       0x07: array('B',
                         []
                         ),
       0x1D: array('B',
                            []
                           )
    },
    "Crc16": {

    },
    "Crc32": {

    }
}
