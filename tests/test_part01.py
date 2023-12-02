import pytest
from day01 import parse_digits, parse_digits_with_words


@pytest.mark.parametrize(
    "line, expected",
    [
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77),
        ("81oneight", 81),
    ],
)
def test_parse_digits(line: str, expected: int):
    assert parse_digits(line) == expected


@pytest.mark.parametrize(
    "line, expected",
    [
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77),
        ("81oneight", 88),
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76),
    ],
)
def test_parse_digits_with_words(line: str, expected: int):
    assert parse_digits_with_words(line) == expected
