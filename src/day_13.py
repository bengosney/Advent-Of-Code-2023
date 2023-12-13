# Standard Library
from itertools import pairwise

# First Party
from utils import draw_grid, no_input_skip, read_input  # noqa

# Third Party
from icecream import ic


def rotate(string: str) -> str:
    grid = [list(line) for line in string.splitlines()]
    return "\n".join(["".join(line) for line in zip(*grid[::-1])])


def reflect(puzzle: str) -> int:
    cols = rotate(puzzle).splitlines()
    for i, (line1, line2) in enumerate(pairwise(cols)):
        leng = len(cols) - 1
        p = min(leng - i, i)
        m = 0 if (leng - i) > i else 1
        if line1 == line2 and cols[(i - p) + m : i + 1] == cols[i + 1 : i + p + 2][::-1]:
            ic("V", i, cols[i - p : i], cols[i : i + p])
            return i + 1

    rows = puzzle.splitlines()
    for i, (line1, line2) in enumerate(pairwise(rows)):
        leng = len(rows) - 1
        p = min(leng - i, i)
        m = 0 if (leng - i) > i else 1
        if line1 == line2 and rows[(i - p) + m : i + 1] == rows[i + 1 : i + p + 2][::-1]:
            ic("H", i, rows[i - p : i], rows[i : i + p])
            return (i + 1) * 100

    raise Exception("No reflections found")


def part_1(input: str) -> int:
    puzzles = input.split("\n\n")
    answer = 0
    for puzzle in puzzles:
        try:
            answer += reflect(puzzle)
        except Exception as e:
            print(puzzle + "\n")
            raise e

    return answer


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 405


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 39939


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
