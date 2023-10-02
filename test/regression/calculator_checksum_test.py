from crc._crc import (
    Calculator,
    Configuration,
)


def test_invalid_calculator_checksum():
    """
    For more details, see also GithubIssue #113 (https://github.com/Nicoretti/crc/issues/113)
    """

    config = Configuration(
        width=16,
        polynomial=0x1021,
        init_value=0xFFFF,
        final_xor_value=0xFFFF,
        reverse_input=False,
        reverse_output=False,
    )
    calculator = Calculator(config)

    expected = 0x1B18
    data = [
        18,
        65,
        116,
        210,
        22,
        0,
        0,
        245,
        121,
        26,
        250,
        44,
        48,
        41,
        135,
        240,
        127,
        165,
        123,
        0,
        96,
    ]
    actual = calculator.checksum(data)

    assert expected == actual
