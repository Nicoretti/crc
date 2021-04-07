import unittest
import timeit


class CrcRegisterBenchTest(unittest.TestCase):

    def test_crc_reg_vs_table_based_reg(self):
        reg = "\n".join([
            "import string",
            "from crc import CrcRegister",
            "from crc import Configuration, Crc8",
            "from collections import namedtuple",
            "CrcTestData = namedtuple('CrcTestData', 'data checksum')",
            "config = Crc8.CCITT",
            "crc_register = CrcRegister(config)",
            "test_suit = [",
            "    CrcTestData(data='', checksum=0x00),",
            "    CrcTestData(data=string.digits[1:], checksum=0xF4),",
            "    CrcTestData(data=string.digits[1:][::-1], checksum=0x91),",
            "    CrcTestData(data=string.digits, checksum=0x45),",
            "    CrcTestData(data=string.digits[::-1], checksum=0x6E),",
            "]",
            "for test in test_suit:",
            "    crc_register.init()",
            "crc_register.update(test.data.encode('utf-8'))",
            "assert test.checksum == crc_register.digest()",
        ])
        reg_times = timeit.repeat(reg, number=100)

        table_reg = "\n".join([
            "import string",
            "from crc import TableBasedCrcRegister",
            "from crc import Configuration, Crc8",
            "from collections import namedtuple",
            "CrcTestData = namedtuple('CrcTestData', 'data checksum')",
            "config = Crc8.CCITT",
            "crc_register = TableBasedCrcRegister(config)",
            "test_suit = [",
            "    CrcTestData(data='', checksum=0x00),",
            "    CrcTestData(data=string.digits[1:], checksum=0xF4),",
            "    CrcTestData(data=string.digits[1:][::-1], checksum=0x91),",
            "    CrcTestData(data=string.digits, checksum=0x45),",
            "    CrcTestData(data=string.digits[::-1], checksum=0x6E),",
            "]",
            "for test in test_suit:",
            "    crc_register.init()",
            "crc_register.update(test.data.encode('utf-8'))",
            "assert test.checksum == crc_register.digest()",
        ])
        table_reg_times = timeit.repeat(table_reg, number=100)
        self.assertTrue(all(map(lambda entry: entry[0] > entry[1], zip(reg_times, table_reg_times))))


if __name__ == '__main__':
    unittest.main()
