# Standard Library
import re

# First Party
from utils import no_input_skip, read_input


def part_1(input: str) -> int:
    total = 0
    for line in input.splitlines():
        if line == "":
            continue
        numbers = [n for n in line if n.isdigit()]
        num = int("".join([numbers[0], numbers[-1]]))
        total += num
    return total


def part_2(input: str) -> int:
    lookup = {r"one": 1, r"two": 2, r"three": 3, r"four": 4, r"five": 5, r"six": 6, r"seven": 7, r"eight": 8, r"nine": 9}

    total = 0
    for line in input.splitlines():
        indexed: list[tuple[int, int]] = []
        for word, number in lookup.items():
            for m in re.finditer(word, line):
                indexed.append((m.start(), number))
        for m in re.finditer(r"\d", line):
            indexed.append((m.start(), int(m.group(0))))

        numbers = [str(i[1]) for i in sorted(indexed, key=lambda i: i[0])]
        num = int("".join([numbers[0], numbers[-1]]))
        total += num
    return total


# -- Tests


def get_example_input_one() -> str:
    return """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""


def get_example_input_two() -> str:
    return """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def test_part_1():
    test_input = get_example_input_one()
    assert part_1(test_input) == 142


def test_part_2():
    test_input = get_example_input_two()
    assert part_2(test_input) == 281


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 55029


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 55686


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
