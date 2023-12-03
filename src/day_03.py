# Standard Library
from collections import defaultdict, deque
from collections.abc import Iterable
from functools import reduce
from itertools import product
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

    class Collector:
        def __init__(self) -> None:
            self.reset()
            self.collected = []

        def reset(self):
            self._collecting = []
            self.valid = False

        def append(self, value: str) -> None:
            self._collecting.append(value)

        def collect(self) -> None:
            if self.valid:
                self.collected.append(int("".join(self._collecting)))
            self.reset()

    collector = Collector()
    for y in grid.height:
        collector.reset()
        for x in grid.width:
            if grid[x, y].isnumeric():
                collector.append(grid[x, y])
                if not collector.valid:
                    for pair in Grid.around(x, y):
                        collector.valid |= grid[pair] != "." and not grid[pair].isnumeric()
            else:
                collector.collect()
        collector.collect()

    return sum(collector.collected)


def part_2(input: str) -> int:
    grid = Grid.build(input)

    def collect_number(x: int, y: int) -> int:
        number: deque[str] = deque()
        cx = x
        while grid[cx, y].isnumeric():
            number.appendleft(grid[cx, y])
            cx -= 1
        cx = x + 1
        while grid[cx, y].isnumeric():
            number.append(grid[cx, y])
            cx += 1
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
