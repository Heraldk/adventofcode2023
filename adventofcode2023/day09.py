from itertools import pairwise

from common import AdventSolution


def parse_sequences(input_file: str) -> list[list[int]]:
    sequences = []
    with open(input_file, "r") as file:
        for line in file.readlines():
            nums = [int(x) for x in line.strip().split(" ")]
            sequences.append(nums)
    return sequences


def expand_sequence(items: list[int]) -> list[list[int]]:
    summary = [items]
    vals = items
    while any([x != 0 for x in vals]):
        new_vals = []
        for x, y in pairwise(vals):
            new_vals.append(y - x)
        vals = new_vals
        summary.append(new_vals)
    return summary


def extrapolate_sequence(expanded_seq: list[list[int]]) -> int:
    last_num = 0
    for seq in reversed(expanded_seq):
        last_num = seq[-1] + last_num
    return last_num


def extrapolate_backwards(expanded_seq: list[list[int]]) -> int:
    last_num = 0
    for seq in reversed(expanded_seq):
        last_num = seq[0] - last_num
    return last_num


class Day09(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        seqs = parse_sequences(input_file)
        extrapolations = [extrapolate_sequence(expand_sequence(seq)) for seq in seqs]
        print(sum(extrapolations))

    def part_two(self, input_file: str):
        seqs = parse_sequences(input_file)
        extrapolations = [extrapolate_backwards(expand_sequence(seq)) for seq in seqs]
        print(sum(extrapolations))
