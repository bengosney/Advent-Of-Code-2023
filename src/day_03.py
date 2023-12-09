# Standard Library
from collections import defaultdict, deque
from collections.abc import Iterable
from functools import reduce
from itertools import count, product, takewhile
from typing import Self

# First Party
from utils import no_input_skip, read_input


class Grid:
    def __init__(self, default: str = ".") -> None:
        self._width: set[int] = set()
        self._height: set[int] = set()
        self._grid: dict[tuple[int, int], str] = defaultdict(lambda: default)

    def __setitem__(self, key: tuple[int, int], value: str) -> None:
        self._width.add(key[0])
        self._height.add(key[1])
        self._grid[key] = value

    def __getitem__(self, key: tuple[int, int]) -> str:
        return self._grid[key]

    @property
    def width(self) -> Iterable[int]:
        return range(min(self._width), max(self._width) + 1)

    @property
    def height(self) -> Iterable[int]:
        return range(min(self._height), max(self._height) + 1)

    @staticmethod
    def around(x: int, y: int) -> Iterable[tuple[int, int]]:
        for pair in product([x - 1, x, x + 1], [y - 1, y, y + 1]):
            if pair != (x, y):
                yield pair

    @classmethod
    def build(cls, input) -> Self:
        grid = cls()
        for y, line in enumerate(input.splitlines()):
            for x, char in enumerate(line):
                grid[x, y] = char
        return grid


def part_1(input: str) -> int:
    grid = Grid.build(input)

    collected: list[int] = []
    collecting: list[str] = []
    valid = False

    def collect():
        nonlocal valid, collecting
        if valid:
            collected.append(int("".join(collecting)))
        collecting.clear()
        valid = False

    for y in grid.height:
        for x in grid.width:
            if grid[x, y].isnumeric():
                collecting.append(grid[x, y])
                if not valid:
                    for pair in Grid.around(x, y):
                        valid |= grid[pair] != "." and not grid[pair].isnumeric()
            else:
                collect()
        collect()

    return sum(collected)


def part_2(input: str) -> int:
    grid = Grid.build(input)

    def collect_number(x: int, y: int) -> int:
        number: deque[str] = deque()

        for i in takewhile(lambda i: grid[i, y].isnumeric(), count(x, -1)):
            number.appendleft(grid[i, y])

        for i in takewhile(lambda i: grid[i, y].isnumeric(), count(x + 1, 1)):
            number.append(grid[i, y])

        return int("".join(number))

    ratio = 0
    for loc in product(grid.height, grid.width):
        if grid[loc] == "*":
            numbers = set()
            for pair in Grid.around(*loc):
                if grid[pair].isnumeric():
                    numbers.add(collect_number(*pair))
            if len(numbers) == 2:
                ratio += reduce(lambda a, b: a * b, numbers)

    return ratio


# -- Tests


def get_example_input() -> str:
    return """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 4361


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 467835


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 544433


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 76314915


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
