from common import AdventSolution


def parse_input(input_file: str) -> list[str]:
    values = []
    with open(input_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            next_row = line.strip().split(",")
            values.extend(next_row)
    return values


def compute_hash(input_str: str) -> int:
    value = 0
    for char in input_str:
        value += ord(char)
        value *= 17
        value %= 256
    return value


def parse_step(step: str) -> tuple[str, str, int]:
    loc = step.find("=")
    if loc >= 0:
        return step[:loc], "=", int(step[loc + 1 :])
    loc = step.find("-")
    if loc >= 0:
        return step[:loc], "-", 0
    assert False


def find_lens(label: str, box: list[tuple[str, int]]) -> int | None:
    for idx, (in_box_label, _) in enumerate(box):
        if in_box_label == label:
            return idx
    return None


def initialisation_sequence(steps: list[str]) -> list[int]:
    boxes = [list() for _ in range(256)]
    for step in steps:
        label, op, focal = parse_step(step)
        box_num = compute_hash(label)
        box = boxes[box_num]
        lens_loc = find_lens(label, box)
        if op == "=":
            if lens_loc is None:
                box.append((label, focal))
            else:
                box[lens_loc] = (label, focal)
        elif op == "-":
            if lens_loc is not None:
                del box[lens_loc]
        else:
            assert False
    return boxes


def compute_focus_power(boxes: list[list[tuple[str, int]]]):
    total_focal = 0
    for box_num, box in enumerate(boxes):
        for slot_num, (_, focal) in enumerate(box):
            total_focal += (box_num + 1) * (slot_num + 1) * focal
    return total_focal


class Day15(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        steps = parse_input(input_file)
        hashes = [compute_hash(step) for step in steps]
        print(sum(hashes))

    def part_two(self, input_file: str):
        steps = parse_input(input_file)
        boxes = initialisation_sequence(steps)
        focal = compute_focus_power(boxes)
        print(focal)
