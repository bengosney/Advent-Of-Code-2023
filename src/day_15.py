# First Party
from utils import no_input_skip, read_input


def hash_algo(input: str) -> int:
    res: int = 0
    for c in input:
        res = ((res + ord(c)) * 17) % 256
    return res


def part_1(input: str) -> int:
    ans = 0
    for part in input.split(","):
        ans += hash_algo(part)

    return ans


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_hash_algo():
    assert hash_algo("HASH") == 52


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 1320


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 520500


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
