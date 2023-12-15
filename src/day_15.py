# Standard Library
import re
from collections import OrderedDict, defaultdict
from functools import reduce

# First Party
from utils import CachingDict, no_input_skip, read_input


def hash_algo(input: str) -> int:
    return reduce(lambda r, c: ((r + ord(c)) * 17) % 256, input, 0)


def part_1(input: str) -> int:
    return sum(hash_algo(part) for part in input.split(","))


def part_2(input: str) -> int:
    regex = re.compile(r"([a-z]+)(=|-)(\d*)")
    boxes: dict[int, dict[str, int]] = defaultdict(OrderedDict)
    hashes = CachingDict[str, int](lambda __key: hash_algo(__key))
    for instruction in regex.finditer(input):
        label, op, num = instruction.groups()
        box_num = hashes[label]
        if op == "-" and label in boxes[box_num]:
            del boxes[box_num][label]
        if op == "=":
            boxes[box_num][label] = int(num)

    power = 0
    for num, contents in boxes.items():
        for slot, focal_length in enumerate(contents.values(), 1):
            power += (num + 1) * slot * focal_length

    return power


# -- Tests


def get_example_input() -> str:
    return "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_hash_algo():
    assert hash_algo("HASH") == 52


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 1320


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 145


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 520500


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 213097


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
