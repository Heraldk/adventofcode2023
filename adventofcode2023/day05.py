from dataclasses import dataclass
from itertools import batched

from common import AdventSolution


@dataclass
class MappingRange:
    destination_start: int
    source_start: int
    map_range: int


@dataclass
class Mapping:
    name: str
    mapping: list[MappingRange]


def parse_input(input_file_name: str) -> tuple[list[int], list[Mapping]]:
    with open(input_file_name, "r") as file:
        lines = file.readlines()
        seeds = [int(seed) for seed in lines[0][7:].split(" ")]
        maps = []

        name = ""
        mappings = []
        for line in lines[2:]:
            if line[0].isdigit():
                nums = [int(num.strip()) for num in line.split(" ")]
                mappings.append(MappingRange(nums[0], nums[1], nums[2]))
            elif line[0] != "\n":
                name = line.strip()
            else:
                maps.append(Mapping(name=name, mapping=mappings))
                name = ""
                mappings = []

        maps.append(Mapping(name=name, mapping=mappings))

    return seeds, maps


def do_one_mapping(source: int, mapping_range: MappingRange) -> int:
    for mapping in mapping_range.mapping:
        if (
            source >= mapping.source_start
            and source < mapping.source_start + mapping.map_range
        ):
            return mapping.destination_start + source - mapping.source_start

    return source


def map_seed_to_destination(seed: int, mapping_ranges: list[MappingRange]) -> int:
    source = seed
    nums = [source]
    for mapping_range in mapping_ranges:
        source = do_one_mapping(source, mapping_range)
        nums.append(source)
    # print(nums)
    return source


def do_one_mapping_range(
    source: int, upper_limit: int, mapping_range: MappingRange
) -> tuple[int, int]:
    limit = None
    for mapping in mapping_range.mapping:
        if (
            source >= mapping.source_start
            and source < mapping.source_start + mapping.map_range
        ):
            dest = mapping.destination_start + source - mapping.source_start
            next_limit = (
                min(
                    source + upper_limit,
                    mapping.source_start + mapping.map_range,
                )
                - source
            )
            return dest, next_limit
        else:
            if source < mapping.source_start:
                next_limit = mapping.source_start - source
                limit = min(next_limit, limit or next_limit)

    if limit is not None:
        return source, limit
    else:
        return source, upper_limit


def map_seed_to_destination_range(
    seed: int, upper_limit: int, mapping_ranges: list[MappingRange]
) -> tuple[int, int]:
    source = seed
    source_upper = upper_limit
    nums = [source]
    for mapping_range in mapping_ranges:
        # print(source, source_upper)
        (source, source_upper) = do_one_mapping_range(
            source, source_upper, mapping_range
        )
        nums.append(source)
    # print(nums)
    # print(source, source_upper)
    return source, source_upper


class Day05(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        seeds, mapping_ranges = parse_input(input_file)
        lowest_dest = None
        for seed in seeds:
            destination = map_seed_to_destination(seed, mapping_ranges)
            lowest_dest = (
                min(lowest_dest, destination)
                if lowest_dest is not None
                else destination
            )
        print(lowest_dest)

    def part_two(self, input_file: str):
        seeds, mapping_ranges = parse_input(input_file)
        lowest_dest = None
        for start, distance in batched(seeds, n=2):
            seed = start
            remaining_distance = distance
            while seed < start + distance:
                destination, interval = map_seed_to_destination_range(
                    seed, remaining_distance, mapping_ranges
                )
                seed += interval
                remaining_distance -= interval
                lowest_dest = (
                    min(lowest_dest, destination)
                    if lowest_dest is not None
                    else destination
                )
        print(lowest_dest)


# Day05().part_two("test_input_files/day05.txt")
