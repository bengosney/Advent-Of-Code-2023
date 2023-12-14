# Standard Library
from collections import defaultdict

# First Party
from utils import no_input_skip, read_input


def part_1(input: str) -> int:
    platform: dict[tuple[int, int], str] = defaultdict(lambda: "!")
    width = 0
    height = 0
    for y, row in enumerate(input.splitlines()):
        height = y + 1
        for x, thing in enumerate(row):
            width = max(width, x + 1)
            platform[x, y] = thing

    for y in range(height):
        for x in range(width):
            if platform[x, y] == "O":
                roll = y
                while platform[x, roll - 1] == ".":
                    roll -= 1
                platform[x, y] = "."
                platform[x, roll] = "O"

    weight = 0
    for y in range(height):
        weight += sum([(height) - y for x in range(width) if platform[x, y] == "O"])
    return weight


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 136


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 105623


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
