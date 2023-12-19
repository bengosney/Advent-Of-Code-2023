# First Party
import re
from dataclasses import dataclass
from typing import Self

from utils import no_input_skip, read_input

Part = dict[str, int]


@dataclass
class Workflow:
    var: str
    op: str
    val: int

    valid: str | Self
    invalid: str | Self

    def test(self, part: Part) -> bool:
        if self.op == ">":
            return part[self.var] > self.val
        return part[self.var] < self.val

    def process(self, part: Part, workflows: dict[str, Self]) -> str:
        if self.test(part):
            result = self.valid
        else:
            result = self.invalid

        if isinstance(result, Workflow):
            result = result.process(part, workflows)

        if len(result) == 1:
            return result

        return workflows[result].process(part, workflows)

    @classmethod
    def parse(cls, rule: str) -> Self:
        half, rest = rule.split(",", 1)
        info, action = half.split(":")
        var = info[0]
        op = info[1]
        val = int(info[2:])

        if "," in rest:
            rest = cls.parse(rest)

        return cls(var, op, val, action, rest)


def parse(puzzle: str) -> tuple[dict[str, Workflow], list[Part]]:
    raw_workflows, raw_parts = puzzle.split("\n\n")

    workflows: dict[str, Workflow] = {}
    for match in re.finditer(r"(\w+){(.*?)}", raw_workflows):
        name, rules = match.groups()
        workflows[name] = Workflow.parse(rules)

    parts = []
    for match in re.finditer(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", raw_parts):
        parts.append(
            {
                "x": int(match.group(1)),
                "m": int(match.group(2)),
                "a": int(match.group(3)),
                "s": int(match.group(4)),
            },
        )

    return workflows, parts


def part_1(puzzle: str) -> int:
    workflows, parts = parse(puzzle)

    ans = 0

    for part in parts:
        if workflows["in"].process(part, workflows) == "A":
            ans += sum(part.values())

    return ans


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 19114


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 368964


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
