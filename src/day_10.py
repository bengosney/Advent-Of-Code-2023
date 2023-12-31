# Standard Library
from collections import defaultdict
from itertools import count, pairwise
from typing import Self

# First Party
from utils import no_input_skip, read_input


class Moves:
    UP = 0, -1
    DOWN = 0, 1
    LEFT = -1, 0
    RIGHT = 1, 0

    @classmethod
    def word(cls: type[Self], move: tuple[int, int]) -> str:
        words: dict[tuple[int, int], str] = {
            cls.UP: "up",
            cls.RIGHT: "right",
            cls.DOWN: "down",
            cls.LEFT: "left",
        }
        return words[move]

    @staticmethod
    def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
        return a[0] + b[0], a[1] + b[1]

    @classmethod
    def directions(cls: type[Self]) -> list[tuple[int, int]]:
        return [cls.UP, cls.RIGHT, cls.DOWN, cls.LEFT]

    @classmethod
    def opposite(cls: type[Self], move: tuple[int, int]) -> tuple[int, int]:
        opposites = {
            cls.LEFT: cls.RIGHT,
            cls.RIGHT: cls.LEFT,
            cls.UP: cls.DOWN,
            cls.DOWN: cls.UP,
        }
        if move in opposites:
            return opposites[move]
        raise Exception(f"Unknown move: {move}")

    @classmethod
    def valid_dirs(cls: type[Self], pipe: str) -> list[tuple[int, int]]:
        valid_dirs = {
            "|": [cls.UP, cls.DOWN],
            "-": [cls.LEFT, cls.RIGHT],
            "F": [cls.RIGHT, cls.DOWN],
            "7": [cls.LEFT, cls.DOWN],
            "L": [cls.UP, cls.RIGHT],
            "J": [cls.UP, cls.LEFT],
            "S": cls.directions(),
        }
        if pipe in valid_dirs:
            return list(valid_dirs[pipe])
        raise Exception(f"Invalid pipe: {pipe}")

    @staticmethod
    def around(x: int, y: int) -> list[tuple[int, int]]:
        return [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]

    @classmethod
    def valid(cls: type[Self], dir: tuple[int, int]) -> list[str]:
        valid = {
            cls.UP: ["|", "F", "7"],
            cls.DOWN: ["|", "J", "L"],
            cls.LEFT: ["-", "F", "L"],
            cls.RIGHT: ["-", "J", "7"],
        }
        if dir in valid:
            return valid[dir]
        raise Exception(f"Invalid dir: {dir}")


def build_path(pipe_map: dict[tuple[int, int], str], start: tuple[int, int]) -> list[tuple[int, int]]:
    current = start
    prev = None
    path: list[tuple[int, int]] = []
    for _ in count():
        for dir in Moves.valid_dirs(pipe_map[current]):
            if dir == prev:
                continue
            n = Moves.add(current, dir)
            if pipe_map[n] == "S":
                path.append(current)
                break
            if pipe_map[n] in Moves.valid(dir):
                path.append(current)
                current = n
                prev = Moves.opposite(dir)
                break
        else:
            raise Exception("No valid move found")
        if pipe_map[n] == "S":
            break

    return path


def part_1(input: str) -> int:
    start = 0, 0
    pipe_map: dict[tuple[int, int], str] = defaultdict(lambda: ".")
    for y, line in enumerate(input.splitlines()):
        for x, char in enumerate(line):
            pipe_map[x, y] = char
            if char == "S":
                start = x, y

    path = build_path(pipe_map, start)
    return len(path) // 2


def path_length(path: list[tuple[int, int]]) -> float:
    length = 0
    for (x1, y1), (x2, y2) in pairwise(path + path[:1]):
        length += (x1 * y2) - (y1 * x2)
    return abs(length) / 2


def part_2(input: str) -> int:
    start = 0, 0
    pipe_map: dict[tuple[int, int], str] = defaultdict(lambda: ".")
    for y, line in enumerate(input.splitlines()):
        for x, char in enumerate(line):
            pipe_map[x, y] = char
            if char == "S":
                start = x, y

    path = build_path(pipe_map, start)
    internal_area = path_length(path)

    return int(internal_area + 1 - (len(path) / 2))


# -- Tests


def get_example_inputs_one() -> tuple[str, str]:
    return (
        """.....
.S-7.
.|.|.
.L-J.
.....""",
        """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""",
    )


def test_part_1() -> None:
    test_input_1, test_input_2 = get_example_inputs_one()
    assert part_1(test_input_1) == 4
    assert part_1(test_input_2) == 8


def get_example_inputs_two():
    return (
        """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""",
        """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........""",
        """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""",
    )


def test_part_2() -> None:
    test_input_1, test_input_2, test_input_3 = get_example_inputs_two()
    assert part_2(test_input_1) == 4
    assert part_2(test_input_2) == 4
    assert part_2(test_input_3) == 8


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 6947


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 273


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
