# First Party
from utils import no_input_skip, read_input


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


def part_2(input: str) -> int:
    pass


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


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 510109797


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
