from dataclasses import dataclass

from common import AdventSolution


@dataclass
class ContinuousSection:
    item: str
    count: int


@dataclass
class Entry:
    input: str
    pattern: list[ContinuousSection]
    match_count: list[int]


def parse_input(input_file: str) -> list[list[ContinuousSection]]:
    ret_value = []
    with open(input_file, "r") as file:
        for line in file.readlines():
            vals = line.strip().split(" ")

            next_row = []
            for char in vals[0]:
                if len(next_row) == 0 or next_row[-1].item != char:
                    next_row.append(ContinuousSection(char, 1))
                else:
                    next_row[-1].count += 1

            input = vals[0]
            match_count = [int(x) for x in vals[1].split(",")]

            ret_value.append(Entry(input, next_row, match_count))
    return ret_value


@dataclass(frozen=True)
class HashKey:
    substr: str
    counts: str


hash_lookup: dict[HashKey, int] = {}


def search_options(substr: str, counts: list[int], prefix: str) -> int:
    if len(substr) == 0 and len(counts) == 0:
        # print(prefix)
        return 1
    if len(substr) == 0 and len(counts) > 0:
        return 0

    key = HashKey(substr, ",".join(map(str, counts)))
    if (val := hash_lookup.get(key)) is not None:
        return val

    if substr[0] == ".":
        return search_options(substr[1:], counts, prefix + ".")
    if substr[0] == "#":
        if len(counts) == 0:
            return 0
        if counts[0] > len(substr):
            return 0
        elif substr[0 : counts[0]].find(".") >= 0:
            return 0
        elif counts[0] == len(substr):
            return search_options("", counts[1:], prefix + substr)
        if substr[counts[0]] == "#":
            return 0
        return search_options(
            substr[counts[0] + 1 :], counts[1:], prefix + substr[: counts[0] + 1]
        )

    assert substr[0] == "?"

    result = search_options("#" + substr[1:], counts, prefix) + search_options(
        "." + substr[1:], counts, prefix
    )
    hash_lookup[key] = result

    return result


class Day12(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        input = parse_input(input_file)
        options = [search_options(val.input, val.match_count, "") for val in input]
        print(options)
        print(sum(options))

    def part_two(self, input_file: str):
        input = parse_input(input_file)
        options = [
            search_options("?".join([val.input] * 5), val.match_count * 5, "")
            for val in input
        ]
        print(options)
        print(sum(options))


# Day12().part_one("test_input_files/day12.txt")
# search_options("?###????????", [3, 2, 1], "")
