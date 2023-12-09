import re
from dataclasses import dataclass
from functools import reduce

from common import AdventSolution


@dataclass
class Game:
    id: int
    games: list[dict[str:int]]


def parse_game(line: str) -> Game:
    parse = re.split(";|:", line)
    game_id = int(parse[0].split()[1])
    games = []
    for game in parse[1:]:
        games_str = re.split(",", game.strip())
        colours = {}
        for colour in games_str:
            vals = re.split(" ", colour.strip())
            colours[vals[1]] = int(vals[0])
        games.append(colours)

    return Game(id=game_id, games=games)


def check_game(max_count: dict[str:int], game: Game) -> bool:
    for game in game.games:
        for colour, count in game.items():
            if max_count.get(colour, 0) < count:
                return False
    return True


def get_min_cubes(game: Game) -> dict[str:int]:
    min_cubes = {}
    for game in game.games:
        for colour, count in game.items():
            min_cubes[colour] = max(min_cubes.get(colour, 0), count)
    return min_cubes


class Day02(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        with open(input_file, "r") as file:
            games = [parse_game(line) for line in file.readlines()]
            filtered_games = filter(
                lambda game: check_game({"red": 12, "green": 13, "blue": 14}, game),
                games,
            )
            print(reduce(lambda x, y: x + y.id, filtered_games, 0))

    def part_two(self, input_file: str):
        with open(input_file, "r") as file:
            games = [parse_game(line) for line in file.readlines()]
            min_cubes = [get_min_cubes(game) for game in games]
            powers = [
                min_cube.get("blue", 0)
                * min_cube.get("red", 0)
                * min_cube.get("green", 0)
                for min_cube in min_cubes
            ]
            print(sum(powers))
            print(sum(powers))
