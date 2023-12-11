# Standard Library
from collections.abc import Generator
from itertools import batched

# First Party
from utils import no_input_skip, read_input
from utils.collections import CachingDict

# Third Party
import pytest


def part_1(input: str) -> int:
    lines = input.splitlines()
    seeds = list(map(int, lines[0].split()[1:]))

    results = []
    for seed in seeds:
        found = False
        for line in lines[2:]:
            if line == "" or ":" in line:
                found = False
                continue

            destination, source, length = list(map(int, line.split()))
            if not found and seed >= source and seed <= source + length:
                seed += destination - source
                found = True

        results.append(seed)

    return min(results)


def split(a: tuple[int, int], b: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
    if a[0] <= b[0] <= a[1] and b[0] != a[0]:
        yield (a[0], b[0] - 1)
        a = (b[0], a[1])
    if a[0] <= b[1] <= a[1] and b[1] != a[1]:
        yield (a[0], b[1])
        a = (b[1] + 1, a[1])
    yield a


def part_2(input: str) -> int:
    lines = [line for line in input.splitlines() if "-to-" not in line]
    seeds = list(map(int, lines[0].split()[1:]))

    results = []
    seed_blocks: list[tuple[int, int]] = []
    for start, count in batched(seeds, 2):
        seed_blocks.append((start, start + count))

    line_cache = CachingDict[str, list[int]](lambda key: list(map(int, key.split())))

    def process_block(block: tuple[int, int], start_line: int = 2, found: bool = False) -> int:
        for i, line in enumerate(lines[start_line:], start_line):
            if line == "":
                found = False
                continue

            destination, source, length = line_cache[line]

            if len(split_blocks := list(split(block, (source, source + length)))) > 1:
                return min(process_block(b, i, found) for b in split_blocks)

            if not found and block[0] >= source and block[1] <= source + length:
                block = block[0] + (destination - source), block[1] + (destination - source)
                found = True

        return min(block)

    for seed_block in seed_blocks:
        results.append(process_block(seed_block))

    return min(results)


# -- Tests


def get_example_input() -> str:
    return """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 35


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ([(20, 30), (40, 50)], [(20, 30)]),
        ([(20, 30), (25, 50)], [(20, 24), (25, 30)]),
        ([(20, 30), (10, 40)], [(20, 30)]),
        ([(20, 30), (10, 25)], [(20, 25), (26, 30)]),
        ([(20, 30), (10, 19)], [(20, 30)]),
        ([(20, 30), (30, 40)], [(20, 29), (30, 30)]),
        ([(20, 30), (20, 40)], [(20, 30)]),
        ([(20, 30), (20, 30)], [(20, 30)]),
        ([(20, 30), (10, 30)], [(20, 30)]),
        ([(20, 30), (10, 20)], [(20, 20), (21, 30)]),
    ],
)
def test_splitting(test_input, expected):
    assert list(split(*test_input)) == expected


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 46


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 510109797


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 9622622


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
