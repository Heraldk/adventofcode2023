from dataclasses import dataclass

from common import AdventSolution


@dataclass(frozen=True)
class Coords:
    x: int
    y: int


DIRECTIONS: dict[str, Coords] = {
    "N": Coords(0, -1),
    "S": Coords(0, 1),
    "E": Coords(1, 0),
    "W": Coords(-1, 0),
}

REVERSE_DIRECTION: dict[str, str] = {"N": "S", "S": "N", "E": "W", "W": "E"}

PIPES: dict[str, dict[str, str]] = {
    "|": {"S": "N", "N": "S"},
    "-": {"E": "W", "W": "E"},
    "L": {"E": "N", "N": "E"},
    "J": {"N": "W", "W": "N"},
    "7": {"S": "W", "W": "S"},
    "F": {"S": "E", "E": "S"},
}


def lookup_map(coords: Coords, map: list[str]) -> str:
    if coords.y < 0 or coords.y >= len(map):
        return "."
    if coords.x < 0 or coords.x >= len(map[coords.y]):
        return "."
    return map[coords.y][coords.x]


def parse_input(input_file: str) -> tuple[list[str], Coords]:
    with open(input_file, "r") as file:
        start = Coords(-1, -1)
        map = [line.strip() for line in file.readlines()]
        for y, line in enumerate(map):
            if (x := line.find("S")) >= 0:
                start = Coords(x, y)

        assert start != Coords(-1, -1)
        start_neighbours = get_start_neighbours(start, map)
        assert len(start_neighbours) == 2
        reverse_dirs = [
            REVERSE_DIRECTION[start_neighbours[0][1]],
            REVERSE_DIRECTION[start_neighbours[1][1]],
        ]
        for pipe, dirs in PIPES.items():
            if reverse_dirs[0] in dirs and reverse_dirs[1] in dirs:
                print(f"setting starting pipe to {pipe}")
                row = list(map[start.y])
                row[start.x] = pipe
                map[start.y] = "".join(row)

        return map, start


def get_start_neighbours(start: Coords, map: list[str]) -> list[Coords]:
    neighbours = []
    for direction, delta in DIRECTIONS.items():
        neighbour_coords = Coords(start.x + delta.x, start.y + delta.y)
        neighbour = lookup_map(neighbour_coords, map)
        if neighbour in PIPES:
            rev_direction = REVERSE_DIRECTION[direction]
            if rev_direction in PIPES[neighbour]:
                neighbours.append((neighbour_coords, rev_direction))

    return neighbours


def follow_loop(start: Coords, map: list[str]) -> tuple[int, dict[Coords, int]]:
    distances_from_start = {}
    distances_from_start[start] = 0

    neighbours = get_start_neighbours(start, map)
    for neighbour_coords, _ in neighbours:
        distances_from_start[neighbour_coords] = 1
    distance_from_start = 1

    while len(neighbours) > 0:
        distance_from_start += 1
        next_neighbours = []
        for coords, incoming_dir in neighbours:
            outgoing_dir = PIPES[lookup_map(coords, map)][incoming_dir]
            delta = DIRECTIONS[outgoing_dir]
            next_coords = Coords(coords.x + delta.x, coords.y + delta.y)
            if next_coords not in distances_from_start:
                distances_from_start[next_coords] = distance_from_start
                next_neighbours.append((next_coords, REVERSE_DIRECTION[outgoing_dir]))
        neighbours = next_neighbours
    # print(distances_from_start)
    return max(distances_from_start.values()), distances_from_start


def fill_area(
    start: Coords,
    visited: dict[Coords, bool],
    pipe_loop: dict[Coords, int],
    map: list[str],
) -> tuple[bool, list[Coords]]:
    explore_list = [start]
    explored = []
    internal = True
    while len(explore_list) > 0:
        next = explore_list.pop(0)
        explored.append(next)
        if next.y < 0 or next.y >= len(map) or next.x < 0 or next.x >= len(map[next.y]):
            explored.extend(explore_list)
            return False, explored
        for _, delta in DIRECTIONS.items():
            neighbour = Coords(next.x + delta.x, next.y + delta.y)
            if neighbour in visited:
                internal = False
            if (
                neighbour not in visited
                and neighbour not in pipe_loop
                and neighbour not in explore_list
                and neighbour not in explored
            ):
                explore_list.append(neighbour)
    return internal, explored


def find_enclosed_areas(
    pipe_loop: dict[Coords, int], map: list[str]
) -> list[dict[Coords, bool]]:
    visited = {}
    num_internal = 0
    enclosed_areas = []
    for pipe_coords in pipe_loop.keys():
        pipe_type = lookup_map(pipe_coords, map)
        for direction, delta in DIRECTIONS.items():
            # look to the directions the pipe doesn't go
            if direction not in PIPES[pipe_type]:
                neighbour_coords = Coords(
                    pipe_coords.x + delta.x, pipe_coords.y + delta.y
                )
                if (
                    neighbour_coords not in visited
                    and neighbour_coords not in pipe_loop
                ):
                    is_internal, explored = fill_area(
                        neighbour_coords, visited, pipe_loop, map
                    )
                    if is_internal:
                        print(explored)
                        num_internal += len(explored)
                        enclosed_areas.append(explored)
                    visited.update({visit: True for visit in explored})
    return enclosed_areas


def find_outside_pipe_piece(pipe_loop: dict[Coords, int], map: list[str]) -> Coords:
    for y in range(len(map)):
        for x in range(len(map[y])):
            if (loc := Coords(x, y)) in pipe_loop:
                return loc
    # should really not get here
    assert False


def lookup_outside_inside(pipe_type: str, incoming_dir: str) -> list[tuple[str, str]]:
    match (pipe_type):
        case "-":
            if incoming_dir == "W":
                return [("N", "O"), ("S", "I")]
            elif incoming_dir == "E":
                return [("S", "O"), ("N", "I")]
        case "|":
            if incoming_dir == "S":
                return [("W", "O"), ("E", "I")]
            elif incoming_dir == "N":
                return [("E", "O"), ("W", "I")]
        case "F":
            if incoming_dir == "S":
                return [("N", "O"), ("W", "O")]
            elif incoming_dir == "E":
                return [("N", "I"), ("W", "I")]
        case "L":
            if incoming_dir == "E":
                return [("S", "O"), ("W", "O")]
            elif incoming_dir == "N":
                return [("S", "I"), ("W", "I")]
        case "7":
            if incoming_dir == "W":
                return [("N", "O"), ("E", "O")]
            elif incoming_dir == "S":
                return [("N", "I"), ("E", "I")]
        case "J":
            if incoming_dir == "N":
                return [("E", "O"), ("S", "O")]
            elif incoming_dir == "W":
                return [("E", "I"), ("S", "I")]
    assert False


# idea here is to track what "side" the outside is. Supposition is that
# the side that the outside is on of the loop is a parity thing that is consistent
# throughout its length.
def follow_loop_parity(
    pipe_loop: dict[Coords, int],
    map: list[str],
    enclosed_areas: list[dict],
) -> dict[Coords, str]:
    categorisation: dict[Coords, str] = {}
    # quick lookup for what the internal areas are, and what index in the enclosed area
    # map they are
    internals = {}
    for idx, area in enumerate(enclosed_areas):
        internals.update({coord: idx for coord in area})

    start = find_outside_pipe_piece(pipe_loop, map)
    # top-left-most pipe must be an "F" piece
    assert lookup_map(start, map) == "F"

    # make sure we start going east to treat the "left" side as outside consistently
    outgoing_dir = "E"
    steps = 0
    current = start
    while steps == 0 or current != start:
        delta = DIRECTIONS[outgoing_dir]
        current = Coords(current.x + delta.x, current.y + delta.y)
        incoming_dir = REVERSE_DIRECTION[outgoing_dir]

        pipe_type = lookup_map(current, map)
        outgoing_dir = PIPES[pipe_type][incoming_dir]
        steps += 1

        # determine which neighbours are outside and which are inside
        neighbours = lookup_outside_inside(pipe_type, incoming_dir)
        for neighbour, inside_or_outside_category in neighbours:
            delta = DIRECTIONS[neighbour]
            loc = Coords(current.x + delta.x, current.y + delta.y)
            # sanity/consistency check
            if loc in categorisation:
                assert inside_or_outside_category == categorisation[loc]
            elif loc in internals:
                area_id = internals[loc]
                for internal_loc in enclosed_areas[area_id]:
                    assert internal_loc not in categorisation
                    categorisation[internal_loc] = inside_or_outside_category

    return categorisation


class Day10(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        map, start = parse_input(input_file)
        max_distance, _ = follow_loop(start, map)
        print(max_distance)

    def part_two(self, input_file: str):
        map, start = parse_input(input_file)
        print(start)
        _, pipe_loop = follow_loop(start, map)
        enclosed_areas = find_enclosed_areas(pipe_loop, map)
        categories = follow_loop_parity(pipe_loop, map, enclosed_areas)
        debug_output(pipe_loop, categories, map)
        count = sum([1 for val in categories.values() if val == "I"])
        print(count)


def debug_output(
    pipe_loop: dict[Coords, int], categories: dict[Coords, str], map: list[str]
):
    for y in range(len(map)):
        for x in range(len(map[y])):
            coords = Coords(x, y)
            if coords in pipe_loop:
                print("*", sep="", end="")
            elif coords in categories:
                print(categories[coords], sep="", end="")
            else:
                print(" ", sep="", end="")
        print()
