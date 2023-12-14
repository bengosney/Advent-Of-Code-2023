# Standard Library
from collections import defaultdict
from enum import Enum

# First Party
from utils import no_input_skip, read_input


def parse(input: str) -> tuple[dict[tuple[int, int], str], int, int]:
    platform: dict[tuple[int, int], str] = defaultdict(lambda: "!")
    width = 0
    height = 0
    for y, row in enumerate(input.splitlines()):
        height = y + 1
        for x, thing in enumerate(row):
            width = max(width, x + 1)
            platform[x, y] = thing
    return platform, width, height


class Directions(Enum):
    NORTH = (0, -1)
    WEST = (-1, 0)
    SOUTH = (0, 1)
    EAST = (1, 0)


def roll(platform: dict[tuple[int, int], str], dir: tuple[int, int], width: int, height: int) -> dict[tuple[int, int], str]:
    match dir:
        case (0, -1):  # North
            y_range = range(height)
            x_range = range(width)
        case (-1, 0):  # West
            y_range = range(height)
            x_range = range(width)
        case (0, 1):  # South
            y_range = range(height, -1, -1)
            x_range = range(width)
        case (1, 0):  # East
            y_range = range(height)
            x_range = range(width, -1, -1)
        case _:
            raise Exception(f"What dir is this? {dir}")
    for y in y_range:
        for x in x_range:
            if platform[x, y] == "O":
                rx, ry = x, y
                while platform[rx + dir[0], ry + dir[1]] == ".":
                    rx += dir[0]
                    ry += dir[1]
                platform[x, y] = "."
                platform[rx, ry] = "O"
    return platform


def part_1(input: str) -> int:
    platform, width, height = parse(input)
    platform = roll(platform, (0, -1), width, height)

    weight = 0
    for y in range(height):
        weight += sum([(height) - y for x in range(width) if platform[x, y] == "O"])
    return weight


def hash_platform(platform: dict[tuple[int, int], str]) -> str:
    return "".join(platform.values())


def cycles(platform: dict[tuple[int, int], str], rounds: int, width: int, height: int) -> dict[tuple[int, int], str]:
    def roll_dirs(platform: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
        for dir in Directions:
            platform = roll(platform, dir.value, width, height)
        return platform

    for _ in range(rounds):
        platform = roll_dirs(platform)
    return platform


def part_2(input: str, rounds: int = 1_000_000_000) -> int:
    platform, width, height = parse(input)

    cache: dict[str, int] = {}

    def roll_dirs(platform: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
        for dir in Directions:
            platform = roll(platform, dir.value, width, height)
        return platform

    for i in range(rounds):
        platform = roll_dirs(platform)

        platform_hash = hash_platform(platform)
        if platform_hash not in cache:
            cache[platform_hash] = i
        else:
            cycle = i - cache[platform_hash]
            idx = cache[platform_hash] + (rounds - cache[platform_hash]) % cycle
            search_hash = ""
            for item in cache.items():
                if item[1] == idx - 1:
                    search_hash = item[0]
            while hash_platform(platform) != search_hash:
                platform = roll_dirs(platform)
            break

    weight = 0
    for y in range(height):
        weight += sum([(height) - y for x in range(width) if platform[x, y] == "O"])
    return weight


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


def build_grid(
    grid: dict[tuple[int, int], str], start: tuple[int, int] | None = None, end: tuple[int, int] | None = None
) -> str:
    _start = start or min(grid)
    _end = end or max(grid)
    rows: list[str] = []
    for y in range(_start[1], _end[1]):
        row: str = ""
        for x in range(_start[0], _end[0]):
            row += grid[(x, y)]
        rows.append(row)
    return "\n".join(rows)


def test_cycle():
    test_input = get_example_input()
    platform, width, height = parse(test_input)
    result = build_grid(cycles(platform, 1, width, height), (0, 0), (width, height))

    answer = """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""

    assert result == answer


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 64


def test_part_2_3_rounds():
    test_input = get_example_input()
    assert part_2(test_input, 3) == 69


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 105623


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 98029


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    test_part_1()
    test_cycle()
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
