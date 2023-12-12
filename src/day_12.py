# Standard Library
import re
from functools import lru_cache

# First Party
from utils import no_input_skip, read_input

no_more = re.compile(r"^\.*#\.*")
match_chunk = re.compile(r"^\.*#+|^\.*\?")


@lru_cache
def find(contiguous_groups: tuple[int, ...], springs: str) -> int:
    if len(contiguous_groups) == 0:
        return 0 if "#" in springs else 1

    if len(springs) == 0 or ("#" not in springs and "?" not in springs):
        return 0

    found = re.match(rf"^\.*[?#]{{{contiguous_groups[0]}}}(?!#)", springs)
    found_chunk = match_chunk.match(springs)

    if found_chunk is None:
        return 0

    if found is None:
        return 0 if no_more.match(springs) else find(contiguous_groups, springs[len(found_chunk[0]) :])

    ans1 = find(contiguous_groups[1:], springs[len(found[0]) + 1 :])
    ans2 = 0 if no_more.match(springs) else find(contiguous_groups, springs[len(found_chunk[0]) :])

    return ans1 + ans2


def part_1(input: str) -> int:
    posibles = 0
    for row in input.splitlines():
        springs, contiguous_groups = row.split()
        posibles += find(tuple(map(int, contiguous_groups.split(","))), springs)

    return posibles


def part_2(input: str) -> int:
    posibles = 0
    for row in input.splitlines():
        springs, contiguous_groups = row.split()
        unfolded_contiguous_groups = list(map(int, contiguous_groups.split(","))) * 5
        posibles += find(tuple(unfolded_contiguous_groups), "?".join([springs] * 5))

    return posibles


# -- Tests


def get_example_input() -> str:
    return """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 21


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 525152


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 7118


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 7030194981795


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    test_part_1()
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
