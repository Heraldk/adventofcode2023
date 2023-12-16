from dataclasses import dataclass

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


@dataclass
class MirrorMap:
    map: list[str]
    beam_directions: dict[Coords : set[str]]


def parse_input(input_file) -> MirrorMap:
    map = MirrorMap(list(), dict())
    with open(input_file, "r") as file:
        for line in file.readlines():
            map.map.append(line.strip())
    return map


def mirror_cell_to_direction(cell_type: str, direction: str) -> list[tuple[str]]:
    match cell_type:
        case ".":
            return [direction]
        case "/":
            if direction == "E":
                return ["N"]
            elif direction == "S":
                return ["W"]
            elif direction == "N":
                return ["E"]
            else:
                assert direction == "W"
                return ["S"]
        case "\\":
            if direction == "E":
                return ["S"]
            elif direction == "S":
                return ["E"]
            elif direction == "N":
                return ["W"]
            else:
                assert direction == "W"
                return ["N"]
        case "-":
            if direction == "E" or direction == "W":
                return [direction]
            assert direction == "S" or direction == "N"
            return ["E", "W"]
        case "|":
            if direction == "N" or direction == "S":
                return [direction]
            assert direction == "E" or direction == "W"
            return ["N", "S"]


def follow_beam(starting_loc: Coords, starting_dir: str, map: MirrorMap) -> MirrorMap:
    explore_list = [(starting_loc, starting_dir)]
    for y in range(len(map.map)):
        for x in range(len(map.map[0])):
            map.beam_directions[Coords(x, y)] = set()

    while len(explore_list) > 0:
        loc, dir = explore_list.pop()
        if dir in map.beam_directions[loc]:
            continue
        map.beam_directions[loc].add(dir)

        cell_type = map.map[loc.y][loc.x]
        for new_direction in mirror_cell_to_direction(cell_type, dir):
            delta = DIR_DELTAS[new_direction]
            new_loc = Coords(loc.x + delta.x, loc.y + delta.y)

            if (
                new_loc.x >= 0
                and new_loc.y >= 0
                and new_loc.x < len(map.map[0])
                and new_loc.y < len(map.map)
            ):
                if new_direction not in map.beam_directions[new_loc]:
                    explore_list.append((new_loc, new_direction))

    return map


def debug_map(map: MirrorMap) -> None:
    for x in range(len(map.map[0])):
        print(x % 10, end="", sep="")
    print()
    for y in range(len(map.map)):
        row = f"{y%10}"
        for x in range(len(map.map[0])):
            coords = Coords(x, y)
            if len(map.beam_directions[coords]) == 0:
                row += map.map[y][x]
            else:
                row += "#"
        print(row)
    print()


def num_energized(map: MirrorMap) -> int:
    return sum(1 for x in map.beam_directions.values() if len(x) > 0)


class Day16(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        map = parse_input(input_file)
        map = follow_beam(Coords(0, 0), "E", map)
        debug_map(map)
        print(num_energized(map))

    def part_two(self, input_file: str):
        map = parse_input(input_file)
        max_energy = 0
        for y in range(len(map.map)):
            map = follow_beam(Coords(0, y), "E", map)
            max_energy = max(max_energy, num_energized(map))
            map = follow_beam(Coords(len(map.map[0]) - 1, y), "W", map)
            max_energy = max(max_energy, num_energized(map))
        for x in range(len(map.map[0])):
            map = follow_beam(Coords(x, 0), "S", map)
            max_energy = max(max_energy, num_energized(map))
            map = follow_beam(Coords(x, len(map.map) - 1), "N", map)
            max_energy = max(max_energy, num_energized(map))
        print(max_energy)


# Day16().part_one("test_input_files/day16.txt")
