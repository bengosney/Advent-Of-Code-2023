# Standard Library
import re
from collections import defaultdict
from itertools import combinations

# First Party
from utils import draw_grid, no_input_skip, read_input  # noqa

# Third Party
from icecream import ic

Point = tuple[int, int]


def rotate(string: str) -> str:
    grid = []
    for y, line in enumerate(string.splitlines()):
        grid.append([])
        for x, char in enumerate(line):
            grid[y].append(char)

    rotated = list(zip(*grid[::-1]))

    output = ""
    for line in rotated:
        output += "".join(line) + "\n"

    return output.strip("\n")


def test_rotate():
    test_str = """
123
456
789"""
    expected = """
741
852
963"""
    assert rotate(test_str.strip("\n")) == expected.strip("\n")


def calc_distance(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def part_1(input: str) -> int:
    expanded = re.sub(r"(^\.+$)", "\\1\n\\1", input, flags=re.MULTILINE)
    expanded = rotate(expanded)
    expanded = re.sub(r"(^\.+$)", "\\1\n\\1", expanded, flags=re.MULTILINE)
    expanded = rotate(expanded)
    expanded = rotate(expanded)
    expanded = rotate(expanded)

    sky: dict[Point, str] = defaultdict(lambda: ".")
    for y, line in enumerate(expanded.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                sky[(x, y)] = char

    galaxies: list[Point] = [k for k, v in sky.items() if v == "#"]
    if len(galaxies) < 15:
        ic(galaxies)
    distance = 0
    for g1, g2 in combinations(galaxies, 2):
        distance += calc_distance(g1, g2)

    return distance - 1


def part_2(input: str, expansion: int = 1_000_000) -> int:
    sky: dict[Point, str] = defaultdict(lambda: ".")
    ys = set()
    xs = set()
    for y, line in enumerate(input.splitlines()):
        ys.add(y)
        for x, char in enumerate(line):
            xs.add(x)
            if char == "#":
                sky[(x, y)] = char

    e_x = []
    for x in range(max(xs) + 1):
        if all([sky[(x, y)] == "." for y in range(max(ys) + 1)]):
            e_x.append(x + (len(e_x) * expansion))
    e_y = []
    for y in range(max(ys) + 1):
        if all([sky[(x, y)] == "." for x in range(max(xs) + 1)]):
            e_y.append(y + (len(e_y) * expansion))

    def expand(point: Point) -> Point:
        x, y = point
        for ex in e_x:
            if x > ex:
                x += expansion - 1
        for ey in e_y:
            if y > ey:
                y += expansion - 1
        return x, y

    galaxies = [k for k, v in sky.items() if v == "#"]
    ic(galaxies)

    galaxies: list[Point] = [expand(k) for k, v in sky.items() if v == "#"]
    ic(galaxies)

    distance = 0
    for g1, g2 in combinations(galaxies, 2):
        distance += calc_distance(g1, g2)

    return distance


# [(4, 0), ( 9, 1), (0, 2), (8, 5), (1, 6), (12, 7), (9, 10), (0, 11), (5, 11)] # correct
# [(4, 0), (10, 1), (0, 2), (8, 5), (1, 6), (12, 7), (10, 10), (0, 11), (5, 11)]
# -- Tests


def get_example_input() -> str:
    return """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 374


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input, 2) == 374
    assert part_2(test_input, 10) == 1030
    assert part_2(test_input, 100) == 8410


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 10231178


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
