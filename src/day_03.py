# Standard Library
from collections import defaultdict, deque
from collections.abc import Iterable
from functools import reduce
from itertools import product

# First Party
from utils import GridType, no_input_skip, read_input


class Grid:
    _width: set[int]
    _height: set[int]

    def __init__(self) -> None:
        self._width = set()
        self._height = set()

    def add(self, x: int, y: int) -> None:
        self._width.add(x)
        self._height.add(y)

    @property
    def width(self):
        return range(min(self._width), max(self._width) + 1)

    @property
    def height(self):
        return range(min(self._height), max(self._height) + 1)

    @staticmethod
    def around(x: int, y: int) -> Iterable[tuple[int, int]]:
        for pair in product([x - 1, x, x + 1], [y - 1, y, y + 1]):
            if pair != (x, y):
                yield pair


def part_1(input: str) -> int:
    grid: GridType = defaultdict(lambda: ".")
    tracker = Grid()
    for y, line in enumerate(input.splitlines()):
        for x, char in enumerate(line):
            tracker.add(x, y)
            grid[x, y] = char

    valid = []
    for y in tracker.height:
        collecting = []
        collecting_valid = False
        for x in tracker.width:
            cur = grid[x, y]
            if cur.isnumeric():
                collecting.append(cur)
                if not collecting_valid:
                    for pair in Grid.around(x, y):
                        collecting_valid |= grid[pair] != "." and not grid[pair].isnumeric()
            else:
                if collecting_valid:
                    valid.append(int("".join(collecting)))
                collecting = []
                collecting_valid = False
        if collecting_valid:
            valid.append(int("".join(collecting)))

    return sum(valid)


def part_2(input: str) -> int:
    grid: GridType = defaultdict(lambda: ".")
    tracker = Grid()
    for y, line in enumerate(input.splitlines()):
        for x, char in enumerate(line):
            tracker.add(x, y)
            grid[x, y] = char

    def collect(x, y) -> int:
        number = deque()
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
    for y in tracker.height:
        for x in tracker.width:
            cur = grid[x, y]
            if cur == "*":
                numbers = set()
                for pair in Grid.around(x, y):
                    if grid[pair].isnumeric():
                        numbers.add(collect(*pair))
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


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
