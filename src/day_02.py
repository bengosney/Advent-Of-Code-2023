# Standard Library
from collections import defaultdict, namedtuple
from collections.abc import Iterable
from dataclasses import dataclass

# First Party
from utils import no_input_skip, read_input

Limit = namedtuple("Limit", ["red", "green", "blue"])


@dataclass(frozen=True, eq=False)
class Game:
    id: int
    red: int
    green: int
    blue: int

    def __le__(self, other: Limit) -> bool:
        return all(
            [
                self.red <= other.red,
                self.green <= other.green,
                self.blue <= other.blue,
            ]
        )

    @property
    def power(self) -> int:
        return self.red * self.green * self.blue


def parse(input: str) -> Iterable[Game]:
    for line in input.splitlines():
        game_id, rest = line.split(":")
        _, id = game_id.split()

        colours = defaultdict(int)
        for round in rest.split(";"):
            for group in round.split(","):
                count, colour = group.split()
                colours[colour] = max(colours[colour], int(count))
        yield Game(int(id), **colours)


def part_1(input: str) -> int:
    games = parse(input)
    limit = Limit(12, 13, 14)
    filtered_games = filter(lambda game: game <= limit, games)
    return sum(map(lambda g: int(g.id), filtered_games))


def part_2(input: str) -> int:
    games = list(parse(input))
    return sum(map(lambda g: g.power, games))


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


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 2286


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 1867


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 84538


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
