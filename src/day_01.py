# Standard Library
import re
from collections.abc import Generator

# First Party
from utils import no_input_skip, read_input


def part_1(input: str) -> int:
    def calibrations() -> Generator[int, None, None]:
        for line in input.splitlines():
            numbers: list[str] = [n for n in line if n.isdigit()]
            yield int("".join([numbers[0], numbers[-1]]))

    return sum(calibrations())


def part_2(input: str) -> int:
    lookup = {k: str(i) for i, k in enumerate(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"], 1)}
    regex = re.compile(rf"(?=({'|'.join(lookup.keys())}|\d))")

    def calibrations() -> Generator[int, None, None]:
        for line in input.splitlines():
            numbers: list[str] = []
            for m in regex.finditer(line):
                char: str = m.group(1)
                numbers.append(lookup[char] if char in lookup else char)
            yield int("".join([numbers[0], numbers[-1]]))

    return sum(calibrations())


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


def test_part_1() -> None:
    test_input = get_example_input_one()
    assert part_1(test_input) == 142


def test_part_2() -> None:
    test_input = get_example_input_two()
    assert part_2(test_input) == 281


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 55029


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 55686


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
