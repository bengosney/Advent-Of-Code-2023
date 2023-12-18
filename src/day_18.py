import re
from collections import Counter, defaultdict, deque
from itertools import pairwise

from utils import no_input_skip, read_input, time_limit

Vec2 = tuple[int, int]


def add(a: Vec2, b: Vec2) -> Vec2:
    return a[0] + b[0], a[1] + b[1]


def mul(a: Vec2, b: Vec2) -> Vec2:
    return a[0] * b[0], a[1] * b[1]


def around(p: Vec2) -> list[Vec2]:
    return [
        (p[0], p[1] + 1),
        (p[0], p[1] - 1),
        (p[0] + 1, p[1]),
        (p[0] - 1, p[1]),
    ]


def part_1(puzzle: str) -> int:
    grid: dict[Vec2, str] = defaultdict(lambda: ".")

    dmap: dict[str, Vec2] = {
        "U": (0, -1),
        "D": (0, 1),
        "L": (-1, 0),
        "R": (1, 0),
    }

    position = (0, 0)
    grid[position] = "#"
    for line in puzzle.splitlines():
        direction_char, number, _colour = line.split()
        direction = dmap[direction_char]
        for _ in range(int(number)):
            position = add(position, direction)
            grid[position] = "#"

    fill: deque[Vec2] = deque([(1, 1)])
    while fill:
        fill_pos = fill.pop()
        grid[fill_pos] = "#"
        for p in around(fill_pos):
            if grid[p] == ".":
                fill.append(p)

    counts = Counter(grid.values()).most_common()

    return counts[0][1]


def internal_area(path: list[Vec2]) -> int:
    length = 0
    for (x1, y1), (x2, y2) in pairwise(path + path[:1]):
        length += (x1 * y2) - (y1 * x2)
    return abs(length) // 2


def part_2(puzzle: str) -> int:
    grid: dict[Vec2, str] = defaultdict(lambda: ".")
    regex = re.compile(r"(\w{5})(\d)")

    dmap: list[Vec2] = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]

    position = (0, 0)
    path: list[Vec2] = [position]
    length = 0
    grid[position] = "#"
    for match in regex.finditer(puzzle):
        hex_distance, direction_num = match.groups()
        direction = dmap[int(direction_num)]
        distance = int(hex_distance, 16)
        length += distance

        move = mul(direction, (distance, distance))
        position = add(position, move)

        path.append(position)

    return internal_area(path) + length // 2 + 1


# -- Tests


def get_example_input() -> str:
    return """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 62


def test_part_2():
    test_input = get_example_input()
    with time_limit(10):
        assert part_2(test_input) == 952408144115


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 35991


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    part_2(get_example_input())
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
