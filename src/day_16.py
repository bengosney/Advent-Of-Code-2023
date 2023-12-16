# Standard Library
from collections import defaultdict, deque
from functools import partial
from typing import Deque

# First Party
from utils import no_input_skip, read_input

Vec2 = tuple[int, int]

UP: Vec2 = (0, -1)
DOWN: Vec2 = (0, 1)
LEFT: Vec2 = (-1, 0)
RIGHT: Vec2 = (1, 0)


def add(a: Vec2, b: Vec2) -> Vec2:
    return a[0] + b[0], a[1] + b[1]


mirror_map_fs = {UP: RIGHT, RIGHT: UP, DOWN: LEFT, LEFT: DOWN}
mirror_map_bs = {UP: LEFT, LEFT: UP, DOWN: RIGHT, RIGHT: DOWN}

Beam = tuple[Vec2, Vec2]


def energize(start: Vec2, direction: Vec2, grid: dict[Vec2, str]) -> int:
    energized: set[Vec2] = set()
    history: set[tuple[Vec2, Vec2]] = set()

    beams: Deque[Beam] = deque([(start, direction)])

    while len(beams):
        current, direction = beams.pop()
        while grid[current] != "!":
            if grid[current] == "!" or (current, direction) in history:
                break

            history.add((current, direction))

            if grid[current] == "|" and direction in [LEFT, RIGHT]:
                beams.append((add(current, UP), UP))
                direction = DOWN

            if grid[current] == "-" and direction in [UP, DOWN]:
                beams.append((add(current, LEFT), LEFT))
                direction = RIGHT

            if grid[current] == "/" and direction in mirror_map_fs:
                direction = mirror_map_fs[direction]

            if grid[current] == "\\" and direction in mirror_map_bs:
                direction = mirror_map_bs[direction]

            energized.add(current)
            if grid[current] == ".":
                grid[current] = "*"

            current = add(current, direction)

    return len(energized)


def part_1(input: str) -> int:
    grid: dict[Vec2, str] = defaultdict(lambda: "!")
    for y, line in enumerate(input.splitlines()):
        for x, c in enumerate(line):
            grid[x, y] = c

    return energize((0, 0), RIGHT, grid)


def part_2(input: str) -> int:
    grid: dict[Vec2, str] = defaultdict(lambda: "!")
    for y, line in enumerate(input.splitlines()):
        for x, c in enumerate(line):
            grid[x, y] = c

    scores: list[int] = []

    starts: list[tuple[Vec2, Vec2]] = []
    max_x, max_y = max(grid)
    for x in range(max_x):
        starts.append(((x, 0), DOWN))
        starts.append(((x, max_y), UP))
    for y in range(max_y):
        starts.append(((0, y), RIGHT))
        starts.append(((max_x, y), LEFT))

    _energize = partial(energize, grid=grid)
    for start in starts:
        scores.append(_energize(*start))

    return max(scores)


# -- Tests


def get_example_input() -> str:
    return r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 46


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 51


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 7482


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 7896


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    test_part_1()
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
