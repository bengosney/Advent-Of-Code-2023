# Standard Library
from collections import defaultdict, deque
from typing import Deque

# First Party
from utils import no_input_skip, read_input

Vec2 = tuple[int, int]

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def add(a: Vec2, b: Vec2) -> Vec2:
    return a[0] + b[0], a[1] + b[1]


mirror_map_fs = {UP: RIGHT, RIGHT: UP, DOWN: LEFT, LEFT: DOWN}
mirror_map_bs = {UP: LEFT, LEFT: UP, DOWN: RIGHT, RIGHT: DOWN}

Beam = tuple[Vec2, Vec2]


def part_1(input: str) -> int:
    grid: dict[Vec2, str] = defaultdict(lambda: "!")
    energized: dict[Vec2, str] = {}
    history: set[tuple[Vec2, Vec2]] = set()
    for y, line in enumerate(input.splitlines()):
        for x, c in enumerate(line):
            grid[x, y] = c

    beams: Deque[Beam] = deque([((0, 0), RIGHT)])

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

            energized[current] = "#"
            if grid[current] == ".":
                grid[current] = "*"

            current = add(current, direction)

    return list(energized.values()).count("#")


def part_2(input: str) -> int:
    pass


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


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 7482


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    test_part_1()
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
