# Standard Library
import re
from collections.abc import Callable
from functools import partial
from itertools import cycle
from math import lcm
from typing import Literal, cast

# First Party
from utils import no_input_skip, read_input

Insts = list[Literal["L", "R"]]
Node = dict[Literal["L", "R"], str]


def solve(current: str, targets: list[str], nodes: dict[str, Node], instructions: Insts) -> int:
    for i, dir in enumerate(cycle(instructions)):
        if current in targets:
            return i
        current = nodes[current][dir]

    raise Exception("This can not happen")


def parse(input: str) -> tuple[Insts, dict[str, Node]]:
    inst_string, node_strings = input.split("\n\n")
    regex = re.compile(r"(\w{3})\s=\s\((\w{3}),\s(\w{3})\)")
    nodes: dict[str, Node] = {}
    for string in node_strings.splitlines():
        if match := regex.match(string):
            nodes[match.group(1)] = {"L": match.group(2), "R": match.group(3)}
    instructions: Insts = cast(Insts, [i for i in inst_string if i in ["R", "L"]])  # Because I know better...

    return instructions, nodes


def get_solver(instructions: Insts, nodes: dict[str, Node], targets: list[str]) -> Callable[[str], int]:
    return partial(solve, instructions=instructions, nodes=nodes, targets=targets)


def part_1(input: str) -> int:
    instructions, nodes = parse(input)

    return solve("AAA", ["ZZZ"], nodes, instructions)


def part_2(input: str) -> int:
    instructions, nodes = parse(input)

    starts = [n for n in nodes if n[-1] == "A"]
    targets = [n for n in nodes if n[-1] == "Z"]
    solver = get_solver(instructions, nodes, targets)

    return lcm(*[solver(c) for c in starts])


# -- Tests


def get_example_input_one() -> str:
    return """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""


def get_example_input_two() -> str:
    return """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


def test_part_1():
    test_input = get_example_input_one()
    assert part_1(test_input) == 2


def test_part_2():
    test_input = get_example_input_two()
    assert part_2(test_input) == 6


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 21797


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 23977527174353


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
