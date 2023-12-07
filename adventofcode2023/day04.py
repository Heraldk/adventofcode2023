from dataclasses import dataclass

from common import AdventSolution


@dataclass
class Card:
    number: int
    winners: set[int]
    numbers: list[int]


def parse_input(input_file_name: str) -> list[Card]:
    cards = []
    with open(input_file_name, "r") as file:
        for line in file.readlines():
            name_card = line.split(":")
            card_num = int(name_card[0].split(" ")[-1])
            numbers_split = name_card[1].strip().split("|")
            cards.append(
                Card(
                    number=card_num,
                    winners={
                        int(number)
                        for number in numbers_split[0].strip().split(" ")
                        if number.isdigit()
                    },
                    numbers={
                        int(number)
                        for number in numbers_split[1].strip().split(" ")
                        if number.isdigit()
                    },
                )
            )
    return cards


def score_card(card: Card) -> int:
    score = 0
    for number in card.numbers:
        if number in card.winners:
            score = score * 2 if score > 0 else 1
    return score


def count_matches(card: Card) -> int:
    count = 0
    for number in card.numbers:
        if number in card.winners:
            count += 1
    return count


class Day04(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        cards = parse_input(input_file)
        scores = [score_card(card) for card in cards]
        print(sum(scores))

    def part_two(self, input_file: str):
        cards = parse_input(input_file)
        card_counts = [1 for card in cards]
        for index, card in enumerate(cards):
            score = count_matches(card)
            for x in range(0, score):
                if x + index + 1 < len(card_counts):
                    card_counts[x + index + 1] += card_counts[index]
        print(sum(card_counts))
