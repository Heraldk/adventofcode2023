import re
from dataclasses import dataclass
from math import lcm
from typing import Callable

from common import AdventSolution


@dataclass
class Node:
    name: str
    left: str
    right: str


def parse_node(line: str) -> Node:
    vals = re.split("=|\\(|\\)|,", line.strip())
    return Node(vals[0].strip(), vals[2].strip(), vals[3].strip())


def parse_input(input_file: str) -> tuple[str, dict[str, Node]]:
    with open(input_file, "r") as file:
        nodes = {}
        lines = file.readlines()
        instructions = lines[0].strip()
        for line in lines[2:]:
            node = parse_node(line)
            nodes[node.name] = node
        return instructions, nodes


def take_step(location: str, direction: str, nodes: dict[str, Node]) -> str:
    if direction == "L":
        return nodes[location].left
    elif direction == "R":
        return nodes[location].right


def follow_path(
    start: int,
    instructions: str,
    end_condition: Callable[[str], bool],
    nodes: dict[str, Node],
    start_index: int = 0,
) -> tuple[int, list[str]]:
    current = start
    index = start_index
    steps = 0
    visited = [start]
    while steps == 0 or not end_condition(current):
        if index >= len(instructions):
            index = 0
        current = take_step(current, instructions[index], nodes)
        visited.append(current)
        index += 1
        steps += 1
    return steps, visited, index


def determine_loop_length(start: str, instructions: str, nodes: dict[str, Node]) -> int:
    steps, visited, index = follow_path(
        start, instructions, lambda x: x[-1] == "Z", nodes
    )
    steps2, visited2, index_2 = follow_path(
        visited[-1], instructions, lambda x: x[-1] == "Z", nodes, index
    )
    if steps == steps2:
        return steps

    raise ValueError("not a simple loop")


class Day08(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        instructions, nodes = parse_input(input_file)
        steps, visited, _ = follow_path(
            "AAA", instructions, lambda x: x == "ZZZ", nodes
        )
        # print(visited)
        print(steps)

    def part_two(self, input_file: str):
        instructions, nodes = parse_input(input_file)
        starting = [loc for loc in nodes.keys() if loc[-1] == "A"]
        print(starting)
        loop_lengths = [
            determine_loop_length(start, instructions, nodes) for start in starting
        ]
        print(loop_lengths)
        print(lcm(*loop_lengths))
        # print(follow_multipath(instructions, nodes))


# Day08().part_two("test_input_files/day08_part2.txt")
# Day08().part_two("test_input_files/day08_part2.txt")
