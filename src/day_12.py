# Standard Library
import re
from functools import lru_cache

# First Party
from utils import no_input_skip, read_input

# Third Party
from icecream import ic


def build_regex(contigs):
    regex = r"^(\?|\.)*"
    for count in contigs:
        regex += rf"(\?|#){{{count}}}(\?|\.)*"
    ic(rf"{regex}$")
    return re.compile(rf"{regex}$")


no_more = re.compile(r"^\.*#\.*")
match_chunk = re.compile(r"^\.*#+|^\.*\?")


@lru_cache
def find(contigs, string):
    if len(contigs) == 0:
        return 0 if "#" in string else 1
    if len(string) == 0 or ("#" not in string and "?" not in string):
        return 0
    found = re.match(rf"^\.*[?#]{{{contigs[0]}}}(?!#)", string)
    found_chunk = match_chunk.match(string)

    if found is None:
        return 0 if no_more.match(string) else find(contigs, string[len(found_chunk[0]) :])

    ans1 = find(contigs[1:], string[len(found[0]) + 1 :])
    ans2 = 0 if no_more.match(string) else find(contigs, string[len(found_chunk[0]) :])

    return ans1 + ans2


def part_1(input: str) -> int:
    posibles = 0
    rows = []
    for row in input.splitlines():
        springs, contig_string = row.split()
        contig = tuple(map(int, contig_string.split(",")))
        rows.append((springs, contig))
        posibles += find(contig, springs)

    return posibles


def part_2(input: str) -> int:
    pass


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


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 7118


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
