# Standard Library
from collections import defaultdict, namedtuple
from collections.abc import Iterable
from dataclasses import dataclass
from functools import total_ordering

# First Party
from utils import no_input_skip, read_input

Limit = namedtuple("Limit", ["max_red", "max_green", "max_blue"])


@total_ordering
@dataclass(frozen=True, eq=False)
class Game:
    id: int
    max_red: int
    max_blue: int
    max_green: int

    def __int__(self) -> int:
        return self.id

    def __add__(self, other) -> int:
        return int(self) + int(other)

    def __eq__(self, other: Limit) -> bool:
        return all(
            [
                self.max_red == other.max_red,
                self.max_green == other.max_green,
                self.max_blue == other.max_blue,
            ]
        )

    def __le__(self, other: Limit) -> bool:
        return all(
            [
                self.max_red <= other.max_red,
                self.max_green <= other.max_green,
                self.max_blue <= other.max_blue,
            ]
        )


def parse(input: str) -> Iterable[Game]:
    for line in input.splitlines():
        game_id, rest = line.split(":")
        _, id = game_id.split()

        colours = defaultdict(int)
        for round in rest.split(";"):
            for group in round.split(","):
                count, colour = group.split()
                colours[f"max_{colour}"] = max(colours[f"max_{colour}"], int(count))
        yield Game(int(id), **colours)


def part_1(input: str) -> int:
    games = list(parse(input))
    limit = Limit(12, 13, 14)
    filtered_games = filter(lambda game: game <= limit, games)
    return sum(map(int, filtered_games))


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 8


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 1867


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
