# Standard Library
import re
from dataclasses import dataclass
from itertools import cycle

# First Party
from utils import no_input_skip, read_input  # noqa


@dataclass(frozen=True)
class Node:
    name: str
    left: str
    right: str


def part_1(input: str) -> int:
    instructions, node_strings = input.split("\n\n")
    regex = re.compile(r"(\w{3})\s=\s\((\w{3}),\s(\w{3})\)")
    nodes = {}
    for string in node_strings.splitlines():
        if match := regex.match(string):
            node = Node(*match.groups())
            nodes[node.name] = node

    steps = 0
    current = "AAA"
    for i in cycle(instructions):
        if i == "L":
            current = nodes[current].left
        else:
            current = nodes[current].right
        steps += 1
        if current == "ZZZ":
            break

    return steps


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 2


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


# @no_input_skip
# def test_part_1_real():
#     real_input = read_input(__file__)
#     assert part_1(real_input) is not None


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
