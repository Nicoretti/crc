# Copyright (c) 2018, Nicola Coretti
# All rights reserved.
import io
import string
import unittest
from collections import namedtuple

import pytest

from crc._crc import (
    Byte,
    Calculator,
    Configuration,
    Crc8,
    Crc16,
    Register,
    TableBasedRegister,
    _generate_template,
    create_lookup_table,
)

Fixture = namedtuple("Fixture", "data checksum")


class TemplateTest(unittest.TestCase):
    def test_generate_template(self):
        test_data = (
            (1, "0x{:01X}"),
            (4, "0x{:01X}"),
            (7, "0x{:02X}"),
            (8, "0x{:02X}"),
            (15, "0x{:04X}"),
            (16, "0x{:04X}"),
            (31, "0x{:08X}"),
            (32, "0x{:08X}"),
            (63, "0x{:016X}"),
            (64, "0x{:016X}"),
        )
        for width, expected in test_data:
            with self.subTest(width=width):
                self.assertEqual(expected, _generate_template(width))

    def test_render_template(self):
        test_data = (
            (1, 1, "0x1"),
            (1, 15, "0xF"),
            (4, 1, "0x1"),
            (8, 1, "0x01"),
            (16, 1, "0x0001"),
            (32, 1, "0x00000001"),
            (64, 1, "0x0000000000000001"),
            (8, 16, "0x10"),
            (16, 16, "0x0010"),
            (32, 16, "0x00000010"),
            (64, 16, "0x0000000000000010"),
            (16, 0x0840, "0x0840"),
            (32, 0x0840, "0x00000840"),
            (64, 0x0840, "0x0000000000000840"),
        )
        for width, value, expected in test_data:
            with self.subTest(width=width):
                template = _generate_template(width)
                self.assertEqual(expected, template.format(value))


class ByteTest(unittest.TestCase):
    def test_index_operator(self):
        byte = Byte(129)
        self.assertEqual(byte[0], 1)
        self.assertEqual(byte[1], 0)
        self.assertEqual(byte[2], 0)
        self.assertEqual(byte[3], 0)
        self.assertEqual(byte[4], 0)
        self.assertEqual(byte[5], 0)
        self.assertEqual(byte[6], 0)
        self.assertEqual(byte[7], 1)

    def test_index_operator_raises_error(self):
        byte = Byte(129)
        with self.assertRaises(IndexError):
            byte[-1]
        with self.assertRaises(IndexError):
            byte[8]

    def test_conversion_to_int(self):
        int_value = 0x01
        byte = Byte(int_value)
        self.assertIsInstance(int(byte), int)
        self.assertEqual(int(byte), int_value)

    def test_is_equal_operator(self):
        for value in range(0, 256):
            self.assertEqual(Byte(value) == Byte(value), True)
            self.assertEqual(Byte(value) == Byte(value + 1), False)

    def test_is_equal_operator_returns_false_for_non_byte_type(self):
        lhs = Byte(1)
        rhs = 1
        self.assertFalse(lhs == rhs)

    def test_hash_byte(self):
        self.assertEqual(hash(1), hash(Byte(1)))

    def test_adding_two_bytes_without_overflow(self):
        lhs = Byte(0x02)
        rhs = Byte(0x10)
        expected_result = Byte(0x12)
        self.assertEqual(lhs + rhs, expected_result)

    def test_adding_an_integer_to_a_byte_without_overflow(self):
        lhs = 0xF0
        rhs = Byte(0x02)
        expected_result = Byte(lhs + int(rhs))
        self.assertEqual(lhs + rhs, expected_result)

    def test_adding_two_bytes_with_overflow(self):
        lhs = Byte(0xFA)
        rhs = Byte(0xFA)
        expected_result = Byte(0xFA + 0xFA)
        self.assertEqual(expected_result, lhs + rhs)

    def test_adding_an_integer_to_a_byte_with_overflow(self):
        lhs = 0xFA
        rhs = Byte(0xFA)
        expected_result = Byte(lhs + int(rhs))
        self.assertEqual(lhs + rhs, expected_result)
        self.assertEqual(lhs + rhs, expected_result)

    def test_instance_based_add(self):
        lhs = Byte(0x00)
        rhs = Byte(0xFA)
        lhs += rhs
        self.assertEqual(lhs._value, rhs._value)

    def test_reversed(self):
        self.assertEqual(int(Byte(0x80).reversed()), 0x01)
        self.assertEqual(int(Byte(0x10).reversed()), 0x08)
        self.assertEqual(int(Byte(0x01).reversed()), 0x80)
        self.assertEqual(int(Byte(0x11).reversed()), 0x88)
        self.assertEqual(int(Byte(0xF0).reversed()), 0x0F)
        self.assertEqual(int(Byte(0x0F).reversed()), 0xF0)


class ConfigurationTest(unittest.TestCase):
    def setUp(self):
        self.width = 8
        self.polynom = 0x07
        self.init_value = 0xFF
        self.final_xor_value = 0xAA
        self.reverse_input = True
        self.reverse_output = True

    def test_init_using_defaults(self):
        configuration = Configuration(self.width, self.polynom)
        self.assertEqual(configuration.width, self.width)
        self.assertEqual(configuration.polynomial, self.polynom)
        self.assertEqual(configuration.init_value, 0)
        self.assertEqual(configuration.final_xor_value, 0)
        self.assertEqual(configuration.reverse_input, False)
        self.assertEqual(configuration.reverse_output, False)

    def test_init(self):
        configuration = Configuration(
            self.width,
            self.polynom,
            self.init_value,
            self.final_xor_value,
            self.reverse_input,
            self.reverse_output,
        )

        self.assertEqual(configuration.width, self.width)
        self.assertEqual(configuration.polynomial, self.polynom)
        self.assertEqual(configuration.init_value, self.init_value)
        self.assertEqual(configuration.final_xor_value, self.final_xor_value)
        self.assertEqual(configuration.reverse_input, self.reverse_input)
        self.assertEqual(configuration.reverse_output, self.reverse_output)


class RegisterTest(unittest.TestCase):
    def setUp(self):
        self._register_types = [Register, TableBasedRegister]

    def test_crc_register_index_error(self):
        config = Crc8.CCITT
        for register_type in self._register_types:
            crc_register = register_type(config)
            with self.assertRaises(IndexError):
                crc_register[10]

    def test_crc8_ccitt(self):
        config = Crc8.CCITT
        for register_type in self._register_types:
            crc_register = register_type(config)
            test_suit = [
                Fixture(data="", checksum=0x00),
                Fixture(data=string.digits[1:], checksum=0xF4),
                Fixture(data=string.digits[1:][::-1], checksum=0x91),
                Fixture(data=string.digits, checksum=0x45),
                Fixture(data=string.digits[::-1], checksum=0x6E),
            ]
            for test in test_suit:
                crc_register.init()
                crc_register.update(test.data.encode("utf-8"))
                self.assertEqual(test.checksum, crc_register.digest())

    def test_crc8_saej1850(self):
        config = Crc8.SAEJ1850
        for register_type in self._register_types:
            crc_register = register_type(config)
            test_suit = [
                Fixture(data="", checksum=0x00),
                Fixture(data=string.digits[1:], checksum=0x37),
                Fixture(data=string.digits[1:][::-1], checksum=0xAA),
                Fixture(data=string.digits, checksum=0x8A),
                Fixture(data=string.digits[::-1], checksum=0x39),
            ]
            for test in test_suit:
                crc_register.init()
                crc_register.update(test.data.encode("utf-8"))
                self.assertEqual(test.checksum, crc_register.digest())

    def test_crc16_ccitt(self):
        config = Crc16.CCITT
        for register_type in self._register_types:
            crc_register = register_type(config)
            test_suit = [
                Fixture(data="", checksum=0x0000),
                Fixture(data=string.digits[1:], checksum=0x31C3),
                Fixture(data=string.digits[1:][::-1], checksum=0x9CAD),
                Fixture(data=string.digits, checksum=0x9C58),
                Fixture(data=string.digits[::-1], checksum=0xD966),
            ]
            for test in test_suit:
                crc_register.init()
                crc_register.update(test.data.encode("utf-8"))
                self.assertEqual(test.checksum, crc_register.digest())

    def test_crc16_modbus(self):
        config = Crc16.MODBUS
        for register_type in self._register_types:
            crc_register = register_type(config)
            test_suit = [
                Fixture(data="", checksum=0xFFFF),
                Fixture(data=string.digits[1:], checksum=0x4B37),
                Fixture(data=string.digits[1:][::-1], checksum=0xC9D3),
                Fixture(data=string.digits, checksum=0x434D),
                Fixture(data=string.digits[::-1], checksum=0x8988),
            ]
            for test in test_suit:
                crc_register.init()
                crc_register.update(test.data.encode("utf-8"))
                self.assertEqual(test.checksum, crc_register.digest())

    def test_crc16_with_reflected_input(self):
        config = Configuration(16, 0x1021, 0, 0, True, False)
        for register_type in self._register_types:
            crc_register = register_type(config)
            test_suit = [
                Fixture(data="", checksum=0x0000),
                Fixture(data=string.digits[1:], checksum=0x9184),
                Fixture(data=string.digits[1:][::-1], checksum=0xF92C),
                Fixture(data=string.digits, checksum=0x76FA),
                Fixture(data=string.digits[::-1], checksum=0x93BA),
            ]
            for test in test_suit:
                crc_register.init()
                crc_register.update(test.data.encode("utf-8"))
                self.assertEqual(test.checksum, crc_register.digest())

    def test_crc16_with_reflected_output(self):
        config = Configuration(16, 0x1021, 0, 0, False, True)
        for register_type in self._register_types:
            crc_register = register_type(config)
            test_suit = [
                Fixture(data="", checksum=0x0000),
                Fixture(data=string.digits[1:], checksum=0xC38C),
                Fixture(data=string.digits[1:][::-1], checksum=0xB539),
                Fixture(data=string.digits, checksum=0x1A39),
                Fixture(data=string.digits[::-1], checksum=0x669B),
            ]
            for test in test_suit:
                crc_register.init()
                crc_register.update(test.data.encode("utf-8"))
                self.assertEqual(test.checksum, crc_register.digest())


class CalculatorTest(unittest.TestCase):
    def test_register_based(self):
        calculator = Calculator(Crc8.CCITT)
        test_suit = [
            Fixture(data="", checksum=0x00),
            Fixture(data=string.digits[1:], checksum=0xF4),
            Fixture(data=string.digits[1:][::-1], checksum=0x91),
            Fixture(data=string.digits, checksum=0x45),
            Fixture(data=string.digits[::-1], checksum=0x6E),
        ]
        for test in test_suit:
            calculator.verify(test.data.encode("utf-8"), test.checksum)

    def test_table_based_calculator(self):
        calculator = Calculator(Crc8.CCITT, True)
        test_suit = [
            Fixture(data="", checksum=0x00),
            Fixture(data=string.digits[1:], checksum=0xF4),
            Fixture(data=string.digits[1:][::-1], checksum=0x91),
            Fixture(data=string.digits, checksum=0x45),
            Fixture(data=string.digits[::-1], checksum=0x6E),
        ]
        for test in test_suit:
            calculator.verify(test.data.encode("utf-8"), test.checksum)


@pytest.mark.parametrize(
    "config,data,expected",
    [
        (Crc8.CCITT, 0, 0x00),
        (Crc8.CCITT, b"", 0x00),
        (Crc8.CCITT, bytearray(), 0x00),
        (Crc8.CCITT, io.BytesIO(b""), 0x00),
        (Crc8.CCITT, (b"", b"", b""), 0x00),
        (Crc8.CCITT, (b"" for i in range(0, 10)), 0x00),
        (Crc8.CCITT, 97, 32),
        (Crc8.CCITT, b"123456789", 0xF4),
        (Crc8.CCITT, bytearray((49, 50, 51, 52, 53, 54, 55, 56, 57)), 0xF4),
        (Crc8.CCITT, io.BytesIO(b"123456789"), 0xF4),
        (Crc8.CCITT, (b"12", b"34", b"56", b"78", b"9"), 0xF4),
        (Crc8.CCITT, (chunk for chunk in (b"12", b"34", b"56", b"78", b"9")), 0xF4),
    ],
)
def test_calculator_with_different_input_types(config, data, expected):
    calculator = Calculator(config)
    assert calculator.checksum(data) == expected


@pytest.mark.parametrize(
    "config,data,expected",
    [
        (Crc8.CCITT, 2.00, TypeError),
        (Crc8.CCITT, "some string", TypeError),
    ],
)
def test_calculator_throws_exception_for_unsupported_input_type(config, data, expected):
    calculator = Calculator(config)
    with pytest.raises(expected):
        calculator.checksum(data)


class CreateLookupTableTest(unittest.TestCase):
    def test_create_crc8_lookup_table(self):
        # fmt: off
        tables = {
            0x07: [
                0x00, 0x07, 0x0E, 0x09, 0x1C, 0x1B, 0x12, 0x15, 0x38, 0x3F, 0x36, 0x31,
                0x24, 0x23, 0x2A, 0x2D,
                0x70, 0x77, 0x7E, 0x79, 0x6C, 0x6B, 0x62, 0x65, 0x48, 0x4F, 0x46, 0x41,
                0x54, 0x53, 0x5A, 0x5D,
                0xE0, 0xE7, 0xEE, 0xE9, 0xFC, 0xFB, 0xF2, 0xF5, 0xD8, 0xDF, 0xD6, 0xD1,
                0xC4, 0xC3, 0xCA, 0xCD,
                0x90, 0x97, 0x9E, 0x99, 0x8C, 0x8B, 0x82, 0x85, 0xA8, 0xAF, 0xA6, 0xA1,
                0xB4, 0xB3, 0xBA, 0xBD,
                0xC7, 0xC0, 0xC9, 0xCE, 0xDB, 0xDC, 0xD5, 0xD2, 0xFF, 0xF8, 0xF1, 0xF6,
                0xE3, 0xE4, 0xED, 0xEA,
                0xB7, 0xB0, 0xB9, 0xBE, 0xAB, 0xAC, 0xA5, 0xA2, 0x8F, 0x88, 0x81, 0x86,
                0x93, 0x94, 0x9D, 0x9A,
                0x27, 0x20, 0x29, 0x2E, 0x3B, 0x3C, 0x35, 0x32, 0x1F, 0x18, 0x11, 0x16,
                0x03, 0x04, 0x0D, 0x0A,
                0x57, 0x50, 0x59, 0x5E, 0x4B, 0x4C, 0x45, 0x42, 0x6F, 0x68, 0x61, 0x66,
                0x73, 0x74, 0x7D, 0x7A,
                0x89, 0x8E, 0x87, 0x80, 0x95, 0x92, 0x9B, 0x9C, 0xB1, 0xB6, 0xBF, 0xB8,
                0xAD, 0xAA, 0xA3, 0xA4,
                0xF9, 0xFE, 0xF7, 0xF0, 0xE5, 0xE2, 0xEB, 0xEC, 0xC1, 0xC6, 0xCF, 0xC8,
                0xDD, 0xDA, 0xD3, 0xD4,
                0x69, 0x6E, 0x67, 0x60, 0x75, 0x72, 0x7B, 0x7C, 0x51, 0x56, 0x5F, 0x58,
                0x4D, 0x4A, 0x43, 0x44,
                0x19, 0x1E, 0x17, 0x10, 0x05, 0x02, 0x0B, 0x0C, 0x21, 0x26, 0x2F, 0x28,
                0x3D, 0x3A, 0x33, 0x34,
                0x4E, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5C, 0x5B, 0x76, 0x71, 0x78, 0x7F,
                0x6A, 0x6D, 0x64, 0x63,
                0x3E, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2C, 0x2B, 0x06, 0x01, 0x08, 0x0F,
                0x1A, 0x1D, 0x14, 0x13,
                0xAE, 0xA9, 0xA0, 0xA7, 0xB2, 0xB5, 0xBC, 0xBB, 0x96, 0x91, 0x98, 0x9F,
                0x8A, 0x8D, 0x84, 0x83,
                0xDE, 0xD9, 0xD0, 0xD7, 0xC2, 0xC5, 0xCC, 0xCB, 0xE6, 0xE1, 0xE8, 0xEF,
                0xFA, 0xFD, 0xF4, 0xF3
            ],

            0x1D:
                [0x00, 0x1D, 0x3A, 0x27, 0x74, 0x69, 0x4E, 0x53, 0xE8, 0xF5, 0xD2, 0xCF,
                 0x9C, 0x81, 0xA6, 0xBB, 0xCD, 0xD0, 0xF7, 0xEA, 0xB9, 0xA4, 0x83, 0x9E,
                 0x25, 0x38, 0x1F, 0x02, 0x51, 0x4C, 0x6B, 0x76, 0x87, 0x9A, 0xBD, 0xA0,
                 0xF3, 0xEE, 0xC9, 0xD4, 0x6F, 0x72, 0x55, 0x48, 0x1B, 0x06, 0x21, 0x3C,
                 0x4A, 0x57, 0x70, 0x6D, 0x3E, 0x23, 0x04, 0x19, 0xA2, 0xBF, 0x98, 0x85,
                 0xD6, 0xCB, 0xEC, 0xF1, 0x13, 0x0E, 0x29, 0x34, 0x67, 0x7A, 0x5D, 0x40,
                 0xFB, 0xE6, 0xC1, 0xDC, 0x8F, 0x92, 0xB5, 0xA8, 0xDE, 0xC3, 0xE4, 0xF9,
                 0xAA, 0xB7, 0x90, 0x8D, 0x36, 0x2B, 0x0C, 0x11, 0x42, 0x5F, 0x78, 0x65,
                 0x94, 0x89, 0xAE, 0xB3, 0xE0, 0xFD, 0xDA, 0xC7, 0x7C, 0x61, 0x46, 0x5B,
                 0x08, 0x15, 0x32, 0x2F, 0x59, 0x44, 0x63, 0x7E, 0x2D, 0x30, 0x17, 0x0A,
                 0xB1, 0xAC, 0x8B, 0x96, 0xC5, 0xD8, 0xFF, 0xE2, 0x26, 0x3B, 0x1C, 0x01,
                 0x52, 0x4F, 0x68, 0x75, 0xCE, 0xD3, 0xF4, 0xE9, 0xBA, 0xA7, 0x80, 0x9D,
                 0xEB, 0xF6, 0xD1, 0xCC, 0x9F, 0x82, 0xA5, 0xB8, 0x03, 0x1E, 0x39, 0x24,
                 0x77, 0x6A, 0x4D, 0x50, 0xA1, 0xBC, 0x9B, 0x86, 0xD5, 0xC8, 0xEF, 0xF2,
                 0x49, 0x54, 0x73, 0x6E, 0x3D, 0x20, 0x07, 0x1A, 0x6C, 0x71, 0x56, 0x4B,
                 0x18, 0x05, 0x22, 0x3F, 0x84, 0x99, 0xBE, 0xA3, 0xF0, 0xED, 0xCA, 0xD7,
                 0x35, 0x28, 0x0F, 0x12, 0x41, 0x5C, 0x7B, 0x66, 0xDD, 0xC0, 0xE7, 0xFA,
                 0xA9, 0xB4, 0x93, 0x8E, 0xF8, 0xE5, 0xC2, 0xDF, 0x8C, 0x91, 0xB6, 0xAB,
                 0x10, 0x0D, 0x2A, 0x37, 0x64, 0x79, 0x5E, 0x43, 0xB2, 0xAF, 0x88, 0x95,
                 0xC6, 0xDB, 0xFC, 0xE1, 0x5A, 0x47, 0x60, 0x7D, 0x2E, 0x33, 0x14, 0x09,
                 0x7F, 0x62, 0x45, 0x58, 0x0B, 0x16, 0x31, 0x2C, 0x97, 0x8A, 0xAD, 0xB0,
                 0xE3, 0xFE, 0xD9, 0xC4]
        }
        # fmt: on
        for polynom, table in tables.items():
            with self.subTest(polynom=polynom, table=table):
                self.assertEqual(table, create_lookup_table(8, polynom))

    def test_create_crc16_lookup_table(self):
        # fmt: off
        tables = {
            0x1021:
                [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,
                 0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
                 0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6,
                 0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
                 0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485,
                 0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
                 0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4,
                 0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
                 0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823,
                 0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
                 0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12,
                 0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
                 0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41,
                 0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
                 0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70,
                 0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
                 0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F,
                 0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
                 0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E,
                 0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
                 0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D,
                 0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
                 0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C,
                 0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
                 0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB,
                 0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
                 0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A,
                 0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
                 0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9,
                 0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
                 0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8,
                 0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0]
        }
        # fmt: on
        for polynom, table in tables.items():
            with self.subTest(polynom=polynom, table=table):
                self.assertEqual(table, create_lookup_table(16, polynom))

    def test_create_crc32_lookup_table(self):
        # fmt: off
        tables = {
            0x4C11DB7:
                [0x00000000, 0x04C11DB7, 0x09823B6E, 0x0D4326D9, 0x130476DC, 0x17C56B6B,
                 0x1A864DB2, 0x1E475005,
                 0x2608EDB8, 0x22C9F00F, 0x2F8AD6D6, 0x2B4BCB61, 0x350C9B64, 0x31CD86D3,
                 0x3C8EA00A, 0x384FBDBD,
                 0x4C11DB70, 0x48D0C6C7, 0x4593E01E, 0x4152FDA9, 0x5F15ADAC, 0x5BD4B01B,
                 0x569796C2, 0x52568B75,
                 0x6A1936C8, 0x6ED82B7F, 0x639B0DA6, 0x675A1011, 0x791D4014, 0x7DDC5DA3,
                 0x709F7B7A, 0x745E66CD,
                 0x9823B6E0, 0x9CE2AB57, 0x91A18D8E, 0x95609039, 0x8B27C03C, 0x8FE6DD8B,
                 0x82A5FB52, 0x8664E6E5,
                 0xBE2B5B58, 0xBAEA46EF, 0xB7A96036, 0xB3687D81, 0xAD2F2D84, 0xA9EE3033,
                 0xA4AD16EA, 0xA06C0B5D,
                 0xD4326D90, 0xD0F37027, 0xDDB056FE, 0xD9714B49, 0xC7361B4C, 0xC3F706FB,
                 0xCEB42022, 0xCA753D95,
                 0xF23A8028, 0xF6FB9D9F, 0xFBB8BB46, 0xFF79A6F1, 0xE13EF6F4, 0xE5FFEB43,
                 0xE8BCCD9A, 0xEC7DD02D,
                 0x34867077, 0x30476DC0, 0x3D044B19, 0x39C556AE, 0x278206AB, 0x23431B1C,
                 0x2E003DC5, 0x2AC12072,
                 0x128E9DCF, 0x164F8078, 0x1B0CA6A1, 0x1FCDBB16, 0x018AEB13, 0x054BF6A4,
                 0x0808D07D, 0x0CC9CDCA,
                 0x7897AB07, 0x7C56B6B0, 0x71159069, 0x75D48DDE, 0x6B93DDDB, 0x6F52C06C,
                 0x6211E6B5, 0x66D0FB02,
                 0x5E9F46BF, 0x5A5E5B08, 0x571D7DD1, 0x53DC6066, 0x4D9B3063, 0x495A2DD4,
                 0x44190B0D, 0x40D816BA,
                 0xACA5C697, 0xA864DB20, 0xA527FDF9, 0xA1E6E04E, 0xBFA1B04B, 0xBB60ADFC,
                 0xB6238B25, 0xB2E29692,
                 0x8AAD2B2F, 0x8E6C3698, 0x832F1041, 0x87EE0DF6, 0x99A95DF3, 0x9D684044,
                 0x902B669D, 0x94EA7B2A,
                 0xE0B41DE7, 0xE4750050, 0xE9362689, 0xEDF73B3E, 0xF3B06B3B, 0xF771768C,
                 0xFA325055, 0xFEF34DE2,
                 0xC6BCF05F, 0xC27DEDE8, 0xCF3ECB31, 0xCBFFD686, 0xD5B88683, 0xD1799B34,
                 0xDC3ABDED, 0xD8FBA05A,
                 0x690CE0EE, 0x6DCDFD59, 0x608EDB80, 0x644FC637, 0x7A089632, 0x7EC98B85,
                 0x738AAD5C, 0x774BB0EB,
                 0x4F040D56, 0x4BC510E1, 0x46863638, 0x42472B8F, 0x5C007B8A, 0x58C1663D,
                 0x558240E4, 0x51435D53,
                 0x251D3B9E, 0x21DC2629, 0x2C9F00F0, 0x285E1D47, 0x36194D42, 0x32D850F5,
                 0x3F9B762C, 0x3B5A6B9B,
                 0x0315D626, 0x07D4CB91, 0x0A97ED48, 0x0E56F0FF, 0x1011A0FA, 0x14D0BD4D,
                 0x19939B94, 0x1D528623,
                 0xF12F560E, 0xF5EE4BB9, 0xF8AD6D60, 0xFC6C70D7, 0xE22B20D2, 0xE6EA3D65,
                 0xEBA91BBC, 0xEF68060B,
                 0xD727BBB6, 0xD3E6A601, 0xDEA580D8, 0xDA649D6F, 0xC423CD6A, 0xC0E2D0DD,
                 0xCDA1F604, 0xC960EBB3,
                 0xBD3E8D7E, 0xB9FF90C9, 0xB4BCB610, 0xB07DABA7, 0xAE3AFBA2, 0xAAFBE615,
                 0xA7B8C0CC, 0xA379DD7B,
                 0x9B3660C6, 0x9FF77D71, 0x92B45BA8, 0x9675461F, 0x8832161A, 0x8CF30BAD,
                 0x81B02D74, 0x857130C3,
                 0x5D8A9099, 0x594B8D2E, 0x5408ABF7, 0x50C9B640, 0x4E8EE645, 0x4A4FFBF2,
                 0x470CDD2B, 0x43CDC09C,
                 0x7B827D21, 0x7F436096, 0x7200464F, 0x76C15BF8, 0x68860BFD, 0x6C47164A,
                 0x61043093, 0x65C52D24,
                 0x119B4BE9, 0x155A565E, 0x18197087, 0x1CD86D30, 0x029F3D35, 0x065E2082,
                 0x0B1D065B, 0x0FDC1BEC,
                 0x3793A651, 0x3352BBE6, 0x3E119D3F, 0x3AD08088, 0x2497D08D, 0x2056CD3A,
                 0x2D15EBE3, 0x29D4F654,
                 0xC5A92679, 0xC1683BCE, 0xCC2B1D17, 0xC8EA00A0, 0xD6AD50A5, 0xD26C4D12,
                 0xDF2F6BCB, 0xDBEE767C,
                 0xE3A1CBC1, 0xE760D676, 0xEA23F0AF, 0xEEE2ED18, 0xF0A5BD1D, 0xF464A0AA,
                 0xF9278673, 0xFDE69BC4,
                 0x89B8FD09, 0x8D79E0BE, 0x803AC667, 0x84FBDBD0, 0x9ABC8BD5, 0x9E7D9662,
                 0x933EB0BB, 0x97FFAD0C,
                 0xAFB010B1, 0xAB710D06, 0xA6322BDF, 0xA2F33668, 0xBCB4666D, 0xB8757BDA,
                 0xB5365D03, 0xB1F740B4]
        }
        # fmt: on
        for polynom, table in tables.items():
            with self.subTest(polynom=polynom, table=table):
                self.assertEqual(table, create_lookup_table(32, polynom))


if __name__ == "__main__":
    unittest.main()
