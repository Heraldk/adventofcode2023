from dataclasses import dataclass

from common import AdventSolution


def flip_map(map: list[str]) -> list[str]:
    cols = [list() for _ in range(len(map[0]))]
    for row in map:
        for idx, char in enumerate(row):
            cols[idx].append(char)
    return ["".join(col) for col in cols]


@dataclass
class MirrorMap:
    map: list[str]


def parse_input(input_file: str) -> list[MirrorMap]:
    maps = []
    with open(input_file, "r") as file:
        map_lines = []
        for line in file.readlines():
            if line.strip() == "":
                maps.append(MirrorMap(map_lines))
                map_lines = []
            else:
                map_lines.append(line.strip())
        if len(map_lines) > 0:
            maps.append(MirrorMap(map_lines))
    return maps


def find_mirror(map: list[str], exclude: int = -1) -> int:
    for x in range(1, len(map)):
        all_match = True
        for i in range(x):
            if x - i - 1 < 0 or x + i >= len(map):
                break
            if map[x - i - 1] != map[x + i]:
                all_match = False
                break
        if all_match and x != exclude:
            return x

    return 0


def flip_smudge(x: int, y: int, map: list[str]) -> list[str]:
    list_copy = [item for item in map]
    list_copy[y] = (
        list_copy[y][:x]
        + ("." if list_copy[y][x] == "#" else "#")
        + list_copy[y][x + 1 :]
    )
    return list_copy


def find_smudged_mirror(map: MirrorMap) -> int:
    original_horizontal = find_mirror(map.map)
    original_vertical = find_mirror(flip_map(map.map))
    for y in range(len(map.map)):
        for x in range(len(map.map[0])):
            new_map = flip_smudge(x, y, map.map)
            # print(new_map)
            horizontal_mirror = find_mirror(new_map, original_horizontal)
            if horizontal_mirror > 0:
                # print(x, y, horizontal_mirror)
                return horizontal_mirror * 100
            vertical_mirror = find_mirror(flip_map(new_map), original_vertical)
            if vertical_mirror > 0:
                # print(x, y, vertical_mirror)
                return vertical_mirror
    return 0


class Day13(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        maps = parse_input(input_file)
        total = 0
        for map in maps:
            horizontal_mirror = find_mirror(map.map)
            vertical_mirror = find_mirror(flip_map(map.map))
            total += horizontal_mirror * 100 + vertical_mirror
        print(total)

    def part_two(self, input_file: str):
        maps = parse_input(input_file)
        total = 0
        for map in maps:
            total += find_smudged_mirror(map)
        print(total)


# Day13().part_one("test_input_files/day13.txt")
