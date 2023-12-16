# Standard Library
import re
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from functools import lru_cache
from typing import Self

# First Party
from utils import no_input_skip, read_input


@dataclass(frozen=True)
class Card:
    id: int
    numbers: frozenset[int]
    winning: frozenset[int]

    @classmethod
    def parse(cls, line: str) -> Self:
        card, numbers = line.split(":")
        _, id = card.split(" ")
        ours, winning = numbers.split("|")
        return cls(
            id=int(id),
            numbers=frozenset(map(int, ours.split())),
            winning=frozenset(map(int, winning.split())),
        )


def parse(input: str) -> Iterable[Card]:
    for line in re.sub(r"[ ]+", " ", input, flags=re.MULTILINE).splitlines():
        yield Card.parse(line)


def part_1(input: str) -> int:
    def scores() -> Generator[int, None, None]:
        for card in parse(input):
            if score := sum([1 for number in card.numbers if number in card.winning]):
                yield int(f"1{'0'*(score - 1)}", 2)

    return sum(scores())


def part_2(input: str) -> int:
    cards = list(parse(input))

    @lru_cache
    def count_cards(card: Card) -> int:
        wins = sum([1 for number in card.numbers if number in card.winning])
        return sum(count_cards(cards[i]) for i in range(card.id, card.id + wins)) + 1

    return sum(count_cards(card) for card in cards)


# -- Tests


def get_example_input() -> str:
    return """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 13


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 30


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 23673


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 12263631


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
