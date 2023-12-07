# Standard Library
from collections import Counter
from dataclasses import dataclass
from functools import cached_property, total_ordering
from itertools import chain
from typing import Self

# First Party
from utils import no_input_skip, read_input


@total_ordering
@dataclass(frozen=True, eq=False)
class Hand:
    cards: list[str]
    bid: int

    @cached_property
    def score(self) -> int:
        counts = Counter(self.cards).most_common()
        mod = 0
        if counts[0][1] == 2 and counts[1][1] == 2:  # two pair
            mod = 1
        if counts[0][1] == 3 and counts[1][1] == 2:  # full house
            mod = 1
        return (counts[0][1] * counts[0][1]) + mod

    @cached_property
    def tiebreak(self) -> list[int]:
        scores = dict({str(v): k + 2 for k, v in enumerate(chain(range(2, 10), ["T", "J", "Q", "K", "A"]))})

        return [scores[card] for card in self.cards]

    def __float__(self) -> float:
        dps = "".join([f"{t:02}" for t in self.tiebreak])
        return float(f"{self.score}.{dps}")

    def __len__(self):
        return len(self.cards)

    def __eq__(self, __value: object) -> bool:
        return float(self) == float(__value)

    def __le__(self, __value: object) -> bool:
        return float(self) <= float(__value)

    @classmethod
    def from_line(cls, line: str) -> Self:
        cards, bid = line.split()
        return cls(list(cards), int(bid))

    @classmethod
    def parse(cls, input: str) -> list[Self]:
        for line in input.splitlines():
            yield cls.from_line(line)


def part_1(input: str) -> int:
    hands = sorted(Hand.parse(input))
    totals = []
    for rank, hand in enumerate(hands, 1):
        totals.append(hand.bid * rank)

    return sum(totals)


def part_2(input: str) -> int:
    hands = sorted(Hand.parse(input))
    totals = []
    for rank, hand in enumerate(hands, 1):
        totals.append(hand.bid * rank)

    return sum(totals)


# -- Tests


def get_example_input() -> str:
    return """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 6440


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 5905


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 248217452


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
