from dataclasses import dataclass
from functools import reduce

from common import AdventSolution


@dataclass
class RaceTimes:
    times: list[int]
    distances: list[int]


def parse_input(input_file_name: str) -> RaceTimes:
    with open(input_file_name, "r") as file:
        lines = file.readlines()
        times = [int(time) for time in lines[0].strip().split(" ") if time.isdigit()]
        distances = [
            int(distance)
            for distance in lines[1].strip().split(" ")
            if distance.isdigit()
        ]
        return RaceTimes(times, distances)


def find_num_winning_strategies(time: int, distance: int) -> int:
    wins = 0
    for t in range(time):
        if t * (time - t) > distance:
            wins += 1

    return wins


class Day06(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        records = parse_input(input_file)
        wins = []
        for time, distance in zip(records.times, records.distances):
            wins.append(find_num_winning_strategies(time, distance))
        print(reduce(lambda x, y: x * y, wins))

    def part_two(self, input_file: str):
        records = parse_input(input_file)
        time = int("".join([str(t) for t in records.times]))
        distance = int("".join([str(d) for d in records.distances]))
        print(find_num_winning_strategies(time, distance))
