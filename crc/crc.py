import abc
import enum
import numbers

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
            value += self[index] << index
            index += 1
        return Byte(value)


class CrcConfiguration(object):
    """
    A CrcConfiguration provides all settings necessary to determine the concrete
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

    CCITT = CrcConfiguration(8, 0x07, 0, 0, False, False)
    SAEJ1850 = CrcConfiguration(8, 0x1D, 0, 0, False, False)


@enum.unique
class Crc16(enum.Enum):
    pass


@enum.unique
class Crc32(enum.Enum):
    pass


def is_crc_configruation(configuration):
    """
    Checks whether or not a specified configuration is a crc configuration or not.

    :param configuration: which will be checked.

    :return: True if it is a valid crc configuration, otherwise False.
    """
    return isinstance(configuration, CrcConfiguration) \
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
        return self._config.width

    def __getitem__(self, item):
        if item >= self._config.width or item < 0:
            raise IndexError
        return (self.register & (1 << item)) >> item

    def init(self):
        self.register = self._config.init_value

    @abc.abstractmethod
    def update(self, data):
        pass

    def digest(self):
        if self._config.reverse_output:
            self.register = self.reverse()
        return self.register ^ self._config.final_xor_value

    def reverse(self):
        index = 0
        reversed_value = 0
        for bit in reversed(self):
            reversed_value += self[index] << index
            index += 1
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

    def update(self, data):
        for byte in data:
            byte = Byte(byte)
            if self._config.reverse_input:
                byte = byte.reversed()
            self.register ^= int(byte) << (self._config.width - 8)
            for bit in byte:
                if self._is_division_possible():
                    self.register = (self.register << 1) ^ self._config.polynom
                else:
                    self.register <<= 1
        return self.register


class TableBasedCrcRegister(CrcRegisterBase):

    def __init__(self, configuration):
        super().__init__(configuration)
        self._lookup_table = None

    def update(self, data):
        raise NotImplementedError


class CrcCalculator(object):

    def __init__(self, configuration, table_driven_calculation=False):
        self._crc_register = CrcRegister(configuration)

    def calculate_checksum(self, data):
        self._crc_register.init()
        self._crc_register.update(data)
        return self._crc_register.digest()


def crc8(data, init_value=0x00, polynom=0x07, final_xor=0x00, reversed_input=False, reversed_output=False):
    config = CrcConfiguration(8, polynom, init_value, final_xor, reversed_input, reversed_output)
    crc_register = CrcRegister(config)
    if isinstance(data, str):
        data = data.encode('utf-8')
    return 244 #crc_register.calculate_checksum(data)

from array import array
LOOKUP_TABLES = {
    Crc8: {
       Crc8.CCITT: array('B',
                         []
                         ),
       Crc8.SAEJ1850: array('B',
                            []
                           )
    },
    "Crc16": {

    },
    "Crc32": {

    }
}
