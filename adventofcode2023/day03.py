from common import AdventSolution

NEIGHBOURS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def has_neighbouring_symbol(x: int, y: int, lines: list[str]):
    for xDelta, yDelta in NEIGHBOURS:
        x1 = x + xDelta
        y1 = y + yDelta
        if y1 >= 0 and y1 < len(lines):
            if x1 >= 0 and x1 < len(lines[y1]):
                if not lines[y1][x1].isdigit() and lines[y1][x1] != ".":
                    return True
    return False


def parse_parts(lines: list[str]) -> list[int]:
    nums_with_parts = []
    for y, line in enumerate(lines):
        cur_num: int | None = None
        is_part = False
        for x, char in enumerate(line):
            if char.isdigit():
                cur_num = cur_num * 10 if cur_num is not None else 0
                cur_num += int(char)
                if not is_part and has_neighbouring_symbol(x, y, lines):
                    is_part = True
            else:
                if is_part and cur_num:
                    nums_with_parts.append(cur_num)
                cur_num = None
                is_part = False
        if is_part and cur_num:
            nums_with_parts.append(cur_num)
    return nums_with_parts


def parse_num(x: int, y: int, lines: list[str]) -> int | None:
    if y < 0 or y >= len(lines) or x < 0 or x >= len(lines[y]):
        return None
    if not lines[y][x].isdigit():
        return None

    left = x
    while left > 0 and lines[y][left - 1].isdigit():
        left -= 1
    right = x
    while right < len(lines[y]) - 1 and lines[y][right + 1].isdigit():
        right += 1
    return int(lines[y][left : right + 1])


def find_neighbouring_numbers(x: int, y: int, lines: list[str]) -> list[int]:
    nums = []
    # parse directly up first, if we don't find a number then parse
    # upper left and upper right separately
    if num := parse_num(x, y - 1, lines):
        nums.append(num)
    else:
        nums.append(parse_num(x - 1, y - 1, lines))
        nums.append(parse_num(x + 1, y - 1, lines))
    nums.append(parse_num(x - 1, y, lines))
    nums.append(parse_num(x + 1, y, lines))
    if num := parse_num(x, y + 1, lines):
        nums.append(num)
    else:
        nums.append(parse_num(x - 1, y + 1, lines))
        nums.append(parse_num(x + 1, y + 1, lines))
    return [num for num in nums if num is not None]


def find_gears(lines: list[str]) -> list[int]:
    gear_powers = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "*":
                numbers = find_neighbouring_numbers(x, y, lines)
                if len(numbers) == 2:
                    print(f"found gear: {numbers[0]}, {numbers[1]}")
                    gear_powers.append(numbers[0] * numbers[1])
    return gear_powers


class Day03(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        with open(input_file, "r") as file:
            # cause of some initial issues: was treating the new line character as a
            # symbol... need to strip that out!
            lines = [line.strip() for line in file.readlines()]
            parts = parse_parts(lines)
            print(sum(parts))

    def part_two(self, input_file: str):
        with open(input_file, "r") as file:
            lines = [line.strip() for line in file.readlines()]
            gears = find_gears(lines)
            print(sum(gears))
