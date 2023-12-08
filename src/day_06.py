# Standard Library
import math
from math import prod

# First Party
from utils import no_input_skip, read_input


def win_count(time: int, distance: int) -> int:
    discriminant = math.sqrt(time**2 - 4 * (distance + 1e-3))

    root1 = math.floor((time + discriminant) / 2)
    root2 = math.ceil((time - discriminant) / 2)

    return (root1 - root2) + 1


def part_1(input: str) -> int:
    times, distances = input.splitlines()
    results = zip([int(t) for t in times.split() if t.isdigit()], [int(d) for d in distances.split() if d.isdigit()])

    wins = []
    for time, distance in results:
        wins.append(win_count(time, distance))

    return prod(wins)


def part_2(input: str) -> int:
    times, distances = input.replace(" ", "").splitlines()
    _, time = times.split(":")
    _, distance = distances.split(":")

    return win_count(int(time), int(distance))


# -- Tests


def get_example_input() -> str:
    return """Time:      7  15   30
Distance:  9  40  200"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 288


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 71503


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 1195150


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 42550411


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
