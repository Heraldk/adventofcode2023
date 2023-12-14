from common import AdventSolution


def parse_input(input_file: str) -> list[list[str]]:
    with open(input_file, "r") as file:
        ret_val = []
        for line in file.readlines():
            ret_val.append(list(line.strip()))
        return ret_val


def tilt_north(map: list[list[str]]) -> list[list[str]]:
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == "O":
                amount_up = 1
                while y - amount_up >= 0 and map[y - amount_up][x] == ".":
                    amount_up += 1
                if amount_up > 1:
                    map[y][x] = "."
                    map[y - amount_up + 1][x] = "O"
    return map


def tilt_south(map: list[list[str]]) -> list[list[str]]:
    for y in range(len(map) - 1, -1, -1):
        for x in range(len(map[y])):
            if map[y][x] == "O":
                amount_down = 1
                while y + amount_down < len(map) and map[y + amount_down][x] == ".":
                    amount_down += 1
                if amount_down > 1:
                    map[y][x] = "."
                    map[y + amount_down - 1][x] = "O"
    return map


def tilt_west(map: list[list[str]]) -> list[list[str]]:
    for x in range(len(map[0])):
        for y in range(len(map)):
            if map[y][x] == "O":
                amount_left = 1
                while x - amount_left >= 0 and map[y][x - amount_left] == ".":
                    amount_left += 1
                if amount_left > 1:
                    map[y][x] = "."
                    map[y][x - amount_left + 1] = "O"
    return map


def tilt_east(map: list[list[str]]) -> list[list[str]]:
    for x in range(len(map[0]) - 1, -1, -1):
        for y in range(len(map)):
            if map[y][x] == "O":
                amount_right = 1
                while (
                    x + amount_right < len(map[0]) and map[y][x + amount_right] == "."
                ):
                    amount_right += 1
                if amount_right > 1:
                    map[y][x] = "."
                    map[y][x + amount_right - 1] = "O"
    return map


def get_map_key(map: list[list[str]]) -> str:
    return "".join("".join(row) for row in map)


def tilt_cycle(map: list[list[str]]) -> list[list[str]]:
    map = tilt_north(map)
    map = tilt_west(map)
    map = tilt_south(map)
    map = tilt_east(map)

    return map


def tilt_cycle_loop(map: list[list[str]], iterations: int) -> list[list[str]]:
    lookup_table = {}
    loop_count: int | None = None
    for x in range(iterations):
        map_key = get_map_key(map)
        if loop_count := lookup_table.get(map_key):
            print("found loop", loop_count, x)
            break
        else:
            lookup_table[map_key] = x
        map = tilt_cycle(map)

    if loop_count is not None:
        loop_length = x - loop_count
        num_loops = (iterations - x) // loop_length
        remaining_iterations = iterations - x - (num_loops * loop_length)
        print(loop_length, num_loops, remaining_iterations)
        for _ in range(remaining_iterations):
            map = tilt_cycle(map)

    return map


def calc_load(map: list[list[str]]) -> int:
    load = 0
    for y in range(len(map)):
        num_boulders = map[y].count("O")
        load += num_boulders * (len(map) - y)
    return load


def debug_map(map: list[list[str]]) -> None:
    for row in map:
        print("".join(row))
    print()


class Day14(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        map = parse_input(input_file)
        tilted_north = tilt_north(map)
        print(calc_load(tilted_north))

    def part_two(self, input_file: str):
        map = parse_input(input_file)
        map = tilt_cycle_loop(map, 1000000000)
        print(calc_load(map))
