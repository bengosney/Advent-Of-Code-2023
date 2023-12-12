# Standard Library
from collections import defaultdict
from itertools import count

# First Party
from utils import no_input_skip, read_input


def extend(seq: list[int]) -> list[int]:
    seqs: dict[int, list[int]] = defaultdict(list)
    seqs[0] = seq
    for i in count():
        for s in range(len(seqs[i]) - 1):
            seqs[i + 1].append(seqs[i][s + 1] - seqs[i][s])

        if all([i == 0 for i in seqs[i]]):
            break

    for n in range(len(seqs) - 2, -1, -1):
        seqs[n] = [seqs[n][0] - seqs[n + 1][0]] + seqs[n] + [seqs[n][-1] + seqs[n + 1][-1]]

    return seqs[0]


def part_1(input: str) -> int:
    answers: list[int] = []
    for line in input.splitlines():
        extended = extend(list(map(int, line.split())))
        answers.append(extended[-1])

    return sum(answers)


def part_2(input: str) -> int:
    answers: list[int] = []
    for line in input.splitlines():
        extended = extend(list(map(int, line.split())))
        answers.append(extended[0])

    return sum(answers)


# -- Tests


def get_example_input() -> str:
    return """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 114


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 2


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 1938800261


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 1112


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
