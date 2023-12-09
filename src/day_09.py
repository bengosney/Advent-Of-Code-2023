# Standard Library
from collections import defaultdict

# First Party
from utils import no_input_skip, read_input


def next_number(seq: list[int]) -> int:
    gaps: dict[int, list[int]] = defaultdict(list)
    i = 0
    gaps[i] = [s for s in seq]
    while i < 1000:
        for s in range(len(gaps[i]) - 1):
            gaps[i + 1].append(gaps[i][s + 1] - gaps[i][s])

        i += 1
        if all([i == 0 for i in gaps[i]]):
            break

    for n in range(i - 1, -1, -1):
        gaps[n].append(gaps[n][-1] + gaps[n + 1][-1])

    return gaps[0][-1]


def part_1(input: str) -> int:
    answers = []
    for line in input.splitlines():
        answers.append(next_number(list(map(int, line.split()))))

    return sum(answers)


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 114


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 1938800261


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
