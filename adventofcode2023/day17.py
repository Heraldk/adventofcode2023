from dataclasses import dataclass, field
from queue import PriorityQueue

from common import AdventSolution


@dataclass(frozen=True)
class Coords:
    x: int
    y: int


DIR_DELTAS = {
    "N": Coords(0, -1),
    "E": Coords(1, 0),
    "W": Coords(-1, 0),
    "S": Coords(0, 1),
}


@dataclass(frozen=True)
class LocWithDirection:
    coords: Coords
    dir: str
    num: int


def get_neighbour(loc: LocWithDirection, direction: str) -> LocWithDirection:
    delta = DIR_DELTAS[direction]
    num = 1 if direction != loc.dir else loc.num + 1
    return LocWithDirection(
        Coords(loc.coords.x + delta.x, loc.coords.y + delta.y), direction, num
    )


DIR_OPTIONS = {
    "N": "NEW",
    "E": "ENS",
    "W": "WNS",
    "S": "SEW",
}


def get_neighbours(
    loc: LocWithDirection, grid: list[list[int]], ultra: bool
) -> list[LocWithDirection]:
    options = []
    for dir in DIR_OPTIONS[loc.dir]:
        neighbour = get_neighbour(loc, dir)
        if (
            neighbour.coords.x >= 0
            and neighbour.coords.y >= 0
            and neighbour.coords.x < len(grid[0])
            and neighbour.coords.y < len(grid)
        ):
            if not ultra and neighbour.num <= 3:
                options.append(neighbour)
            elif (
                ultra
                and neighbour.num <= 10
                and (loc.num == 0 or neighbour.dir == loc.dir or loc.num >= 4)
            ):
                options.append(neighbour)
    return options


@dataclass(order=True)
class SearchItem:
    distance: int
    item: LocWithDirection = field(compare=False)


def find_path(start: Coords, end: Coords, grid: list[list[int]], ultra: bool):
    visited: dict[LocWithDirection, int] = {}
    queue = PriorityQueue()
    queue.put(SearchItem(distance=0, item=LocWithDirection(start, "S", 0)))

    while not queue.empty():
        next = queue.get()
        if next.item in visited:
            assert visited[next.item] <= next.distance
            continue
        visited[next.item] = next.distance
        if next.item.coords == end:
            return next.distance

        neighbours = get_neighbours(next.item, grid, ultra)
        for neighbour in neighbours:
            distance = next.distance + grid[neighbour.coords.y][neighbour.coords.x]
            if neighbour in visited:
                assert visited[neighbour] <= distance
            else:
                queue.put(SearchItem(distance=distance, item=neighbour))

    return None


def parse_grid(input_file: str) -> list[list[int]]:
    grid = []
    with open(input_file, "r") as file:
        for line in file.readlines():
            vals = [int(x) for x in line.strip()]
            grid.append(vals)
        return grid


class Day17(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        grid = parse_grid(input_file)
        print(
            find_path(
                Coords(0, 0), Coords(len(grid[0]) - 1, len(grid) - 1), grid, False
            )
        )

    def part_two(self, input_file: str):
        grid = parse_grid(input_file)
        print(
            find_path(Coords(0, 0), Coords(len(grid[0]) - 1, len(grid) - 1), grid, True)
        )


# Day17().part_one("test_input_files/day17.txt")
