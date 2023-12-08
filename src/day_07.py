# Standard Library
from collections import Counter
from collections.abc import Generator
from dataclasses import dataclass
from functools import cached_property, lru_cache, total_ordering
from itertools import chain
from typing import Self

# First Party
from utils import no_input_skip, read_input


@total_ordering
@dataclass(frozen=True, eq=False, unsafe_hash=True)
class Hand:
    cards: tuple[str, ...]
    bid: int
    joker: bool = False

    @staticmethod
    def _score_hand(counts: list[tuple[str, int]]) -> int:
        mod = 0
        if counts[0][1] == 2 and counts[1][1] == 2:  # two pair
            mod = 1
        if counts[0][1] == 3 and counts[1][1] == 2:  # full house
            mod = 1
        return (counts[0][1] * counts[0][1]) + mod

    @cached_property
    def score(self) -> int:
        return self._score_hand(Counter(self.cards).most_common())

    @cached_property
    def best_score(self) -> int:
        joker_count = sum([1 for c in self.cards if c == "J"])
        score = self.score
        if joker_count > 0 and joker_count < 5:
            counts = Counter([c for c in self.cards if c != "J"]).most_common()
            counts[0] = (counts[0][0], counts[0][1] + joker_count)
            score = self._score_hand(counts)

        return score

    @cached_property
    def tiebreak(self) -> str:
        if not self.joker:
            scores = dict({str(v): k + 2 for k, v in enumerate(chain(range(2, 10), ["T", "J", "Q", "K", "A"]))})
        else:
            scores = dict({str(v): k + 2 for k, v in enumerate(chain(["J"], range(2, 10), ["T", "Q", "K", "A"]))})
        return "".join([f"{scores[card]:02}" for card in self.cards])

    @lru_cache
    def __float__(self) -> float:
        return float(f"{self.score if not self.joker else self.best_score}.{self.tiebreak}")

    def __len__(self):
        return len(self.cards)

    def __eq__(self, __value: object) -> bool:
        return float(self) == __value

    def __le__(self, __value: object) -> bool:
        if isinstance(__value, self.__class__):
            return float(self) <= float(__value)
        return NotImplemented

    @classmethod
    def from_line(cls, line: str, joker: bool = False) -> Self:
        cards, bid = line.split()
        return cls(tuple(list(cards)), int(bid), joker)

    @classmethod
    def parse(cls, input: str, joker: bool = False) -> Generator[Self, None, None]:
        for line in input.splitlines():
            yield cls.from_line(line, joker)


def part_1(input: str) -> int:
    hands = sorted(Hand.parse(input))
    totals = []
    for rank, hand in enumerate(hands, 1):
        totals.append(hand.bid * rank)

    return sum(totals)


def part_2(input: str) -> int:
    hands = sorted(Hand.parse(input, True))
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


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 245576185


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
