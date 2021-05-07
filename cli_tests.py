#!/usr/bin/env python3
#
# Copyright (c) 2021, Nicola Coretti
# All rights reserved.
import unittest
from unittest.mock import patch, call
from crc import main


class CliTests(unittest.TestCase):

    def test_cli_no_arguments_provided(self):
        expected_exit_code = -1
        argv = []
        with patch('sys.exit') as exit_mock:
            main(argv)
            self.assertTrue(exit_mock.called)
            self.assertEqual(exit_mock.call_args, (call(expected_exit_code)))

    def test_table_subcommand_with_no_additional_arguments(self):
        expected_exit_code = -1
        argv = ['table']
        with patch('sys.exit') as exit_mock:
            main(argv)
            self.assertTrue(exit_mock.called)
            self.assertEqual(exit_mock.call_args, (call(expected_exit_code)))


if __name__ == '__main__':
    unittest.main()
