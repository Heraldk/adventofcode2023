import re

from common import AdventSolution

STRING_NAME_TO_DIGIT = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def parse_digits(line: str) -> int:
    digits = re.findall("\\d", line)
    return int(digits[0]) * 10 + int(digits[-1])


def parse_digits_with_words(line: str):
    forward_str = "|".join(STRING_NAME_TO_DIGIT.keys())
    nums = re.findall(f"{forward_str}|\\d", line)
    first_digit = STRING_NAME_TO_DIGIT.get(nums[0]) or int(nums[0])

    # trick to part two: need to parse string in reverse to find the last number
    # if we don't do this trick, then a string like oneight doesn't work as the string
    # "one" is parsed first which consumes the "e" and we don't get the word eight.

    # the [::-1] is a nice way to just step backwards through a string so it effectively
    # lets us look at the string reversed
    reverse_str = "|".join(key[::-1] for key in STRING_NAME_TO_DIGIT.keys())
    reverse_nums = re.findall(f"{reverse_str}|\\d", line[::-1])
    second_digit = STRING_NAME_TO_DIGIT.get(reverse_nums[0][::-1]) or int(
        reverse_nums[0]
    )
    return first_digit * 10 + second_digit


class Day01(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        with open(input_file, "r") as file:
            nums = [parse_digits(line) for line in file.readlines()]
            print(sum(nums))

    def part_two(self, input_file: str):
        with open(input_file, "r") as file:
            nums = [parse_digits_with_words(line) for line in file.readlines()]
            print(sum(nums))
