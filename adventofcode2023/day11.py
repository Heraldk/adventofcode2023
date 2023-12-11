from dataclasses import dataclass
from itertools import combinations

from common import AdventSolution


@dataclass
class Coords:
    x: int
    y: int


@dataclass
class Map:
    map: list[str]
    empty_cols: set[int]
    empty_rows: set[int]
    galaxies: list[Coords]


def parse_input(input_file: str) -> Map:
    rows = []
    with open(input_file, "r") as file:
        for line in file.readlines():
            rows.append(line.strip())

    empty_rows = set()
    empty_cols = {x for x in range(len(rows[0]))}
    galaxies = []

    for y in range(len(rows)):
        if rows[y] == ("." * len(rows[0])):
            empty_rows.add(y)

        for x in range(len(rows[0])):
            if rows[y][x] == "#":
                if x in empty_cols:
                    empty_cols.remove(x)
                galaxies.append(Coords(x, y))

    return Map(
        map=rows, empty_cols=empty_cols, empty_rows=empty_rows, galaxies=galaxies
    )


def between(val: int, is_col: bool, gal1: Coords, gal2: Coords) -> bool:
    if is_col:
        return (val > gal1.x and val < gal2.x) or (val > gal2.x and val < gal1.x)
    else:
        return (val > gal1.y and val < gal2.y) or (val > gal2.y and val < gal1.y)


def find_all_pairs_shortest_paths(map: Map, age_multiplier: int) -> int:
    total_distance = 0
    for galaxy1, galaxy2 in combinations(map.galaxies, 2):
        # distance between two galaxies is the manhattan distance plus double counting
        # any empty spaces or columns crossed
        empty_cols_crossed = sum(
            [1 for col in map.empty_cols if between(col, True, galaxy1, galaxy2)]
        )
        empty_rows_crossed = sum(
            [1 for row in map.empty_rows if between(row, False, galaxy1, galaxy2)]
        )
        distance = (
            abs(galaxy1.x - galaxy2.x)
            + empty_cols_crossed * (age_multiplier - 1)
            + abs(galaxy2.y - galaxy1.y)
            + empty_rows_crossed * (age_multiplier - 1)
        )
        # print(galaxy1, galaxy2, distance)

        total_distance += distance
    return total_distance


class Day11(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        map = parse_input(input_file)
        print(find_all_pairs_shortest_paths(map, 2))

    def part_two(self, input_file: str):
        map = parse_input(input_file)
        print(find_all_pairs_shortest_paths(map, 1_000_000))
