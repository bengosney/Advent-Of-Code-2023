# Standard Library
from collections import defaultdict
from enum import Enum

# First Party
from utils import no_input_skip, read_input, time_limit

# Third Party
from icecream import ic


class Directions(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


def roll(platform: dict[tuple[int, int], str], dir: tuple[int, int], width: int, height: int) -> dict[tuple[int, int], str]:
    for y in range(height):
        for x in range(width):
            if platform[x, y] == "O":
                rx, ry = x, y
                while platform[rx + dir[0], ry + dir[1]] == ".":
                    rx += dir[0]
                    ry += dir[1]
                platform[x, y] = "."
                platform[rx, ry] = "O"
    return platform


def part_1(input: str) -> int:
    platform: dict[tuple[int, int], str] = defaultdict(lambda: "!")
    width = 0
    height = 0
    for y, row in enumerate(input.splitlines()):
        height = y + 1
        for x, thing in enumerate(row):
            width = max(width, x + 1)
            platform[x, y] = thing

    platform = roll(platform, (0, -1), width, height)

    weight = 0
    for y in range(height):
        weight += sum([(height) - y for x in range(width) if platform[x, y] == "O"])
    return weight


def hash_platform(platform: dict[tuple[int, int], str]) -> str:
    return "".join(platform.values())


def part_2(input: str) -> int:
    platform: dict[tuple[int, int], str] = defaultdict(lambda: "!")
    width = 0
    height = 0
    for y, row in enumerate(input.splitlines()):
        height = y + 1
        for x, thing in enumerate(row):
            width = max(width, x + 1)
            platform[x, y] = thing

    cache: dict[str, int] = {}

    rounds = 1_000_000_000

    def roll_dirs(platform: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
        for dir in Directions:
            platform = roll(platform, dir.value, width, height)
        return platform

    for i in range(rounds):
        ic("round", i)
        platform = roll_dirs(platform)
        platform_hash = hash_platform(platform)
        if platform_hash not in cache:
            cache[platform_hash] = i
        else:
            cycle = i - cache[platform_hash]
            idx = cache[platform_hash] + (rounds - cache[platform_hash]) % cycle
            search_hash = ""
            for item in cache.items():
                if item[1] == idx:
                    search_hash = item[0]
            while hash_platform(platform) != search_hash:
                for _ in range(rounds % idx):
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


def test_part_2():
    test_input = get_example_input()
    with time_limit(10):
        assert part_2(test_input) == 64


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

    # print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
