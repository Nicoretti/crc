"""
This module contains regression tests regarding the issue of unstable return values from the `digest` function.
The tests ensure that the `digest` function consistently returns the expected output for given inputs.
For more context and a detailed discussion of the problem, refer to the GitHub issue:
https://github.com/Nicoretti/crc/issues/151
"""

import itertools

import pytest

import crc


def test_original_regression():
    reg = crc.Register(crc.Crc8.BLUETOOTH)
    reg.init()
    reg.update(b"Hello World!")

    times = 10
    expected = [81 for _ in range(0, times)]
    actual = [reg.digest() for _ in range(0, times)]

    assert actual == expected


@pytest.mark.parametrize(
    "configuration,times,expected",
    [
        (config, 10, crc.Calculator(config).checksum(b"Hello World!"))
        for config in itertools.chain(crc.Crc8, crc.Crc16, crc.Crc32, crc.Crc64)
    ],
)
def test_digest_is_stable(configuration, times, expected):
    expected = [expected for _ in range(times)]

    reg = crc.Register(configuration)
    reg.init()
    reg.update(b"Hello World!")
    actual = [reg.digest() for _ in range(times)]

    assert actual == expected
