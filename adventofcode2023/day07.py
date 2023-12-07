from collections import Counter
from dataclasses import dataclass
from enum import IntEnum

from common import AdventSolution


class HandRank(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


@dataclass
class CamelPokerHand:
    hand: str
    bid: int
    hand_class: HandRank


def determine_hand_rank(hand: str, joker: bool) -> HandRank:
    counter = Counter(hand)
    most_common = counter.most_common()

    joker_count = 0
    if joker:
        joker_count = counter["J"]
        counter.subtract(Counter(J=joker_count))
        if counter["J"] == 0:
            del counter["J"]
        most_common = counter.most_common()

    if joker_count == 5 or most_common[0][1] + joker_count == 5:
        return HandRank.FIVE_OF_A_KIND
    elif most_common[0][1] + joker_count == 4:
        return HandRank.FOUR_OF_A_KIND
    elif most_common[0][1] + joker_count == 3:
        if most_common[1][1] == 2:
            return HandRank.FULL_HOUSE
        else:
            return HandRank.THREE_OF_A_KIND
    elif most_common[0][1] + joker_count == 2:
        if most_common[1][1] == 2:
            return HandRank.TWO_PAIR
        else:
            return HandRank.ONE_PAIR
    else:
        if len(most_common) != 5 or joker_count > 0:
            print(hand)
            print(most_common)
        assert len(most_common) == 5
        assert joker_count == 0
        return HandRank.HIGH_CARD


def parse_input(input_file: str, joker: bool = False) -> list[CamelPokerHand]:
    hands = []
    with open(input_file, "r") as file:
        for line in file.readlines():
            vals = line.strip().split(" ")
            hands.append(
                CamelPokerHand(
                    vals[0], int(vals[1]), determine_hand_rank(vals[0], joker)
                )
            )
    return hands


def card_to_rank(card: str, joker: bool = False) -> int:
    match (card):
        case "A":
            return 14
        case "K":
            return 13
        case "Q":
            return 12
        case "J":
            return 11 if not joker else 1
        case "T":
            return 10
        case _:
            return int(card)


class Day07(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        hands = parse_input(input_file)
        hands.sort(
            key=lambda x: (
                x.hand_class,
                card_to_rank(x.hand[0]),
                card_to_rank(x.hand[1]),
                card_to_rank(x.hand[2]),
                card_to_rank(x.hand[3]),
                card_to_rank(x.hand[4]),
            )
        )
        total_winnings = 0
        for id, hand in enumerate(hands):
            total_winnings += (id + 1) * hand.bid
        print(total_winnings)

    def part_two(self, input_file: str):
        hands = parse_input(input_file, True)
        hands.sort(
            key=lambda x: (
                x.hand_class,
                card_to_rank(x.hand[0], True),
                card_to_rank(x.hand[1], True),
                card_to_rank(x.hand[2], True),
                card_to_rank(x.hand[3], True),
                card_to_rank(x.hand[4], True),
            )
        )
        total_winnings = 0
        for id, hand in enumerate(hands):
            total_winnings += (id + 1) * hand.bid
        print(total_winnings)
