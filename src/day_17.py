# First Party
import heapq
from typing import NamedTuple

from utils import draw_grid, read_input, time_limit

Vec2 = tuple[int, int]
Grid = dict[Vec2, int]


class Node(NamedTuple):
    loss: int
    position: Vec2
    direction: int
    chain: int
    history: list[Vec2]

    def __repr__(self) -> str:
        return str(self.loss)


def around(point: Vec2) -> tuple[Vec2, Vec2, Vec2, Vec2]:
    x, y = point
    return ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1))


def part_1(puzzle: str) -> int:
    grid: Grid = {}
    for y, line in enumerate(puzzle.splitlines()):
        for x, loss in enumerate(line):
            grid[x, y] = int(loss)

    queue = [Node(0, (0, 0), 0, 1, [])]
    heapq.heapify(queue)
    visited: dict[tuple[Vec2, int], int] = {}

    end = max(grid)

    while queue:
        node = heapq.heappop(queue)
        key = (node.position, node.direction)  # , node.chain)
        if key in visited:  # and best[key] <= node.loss:
            continue
        if node.position == end:
            dmap = [">", "v", "<", "^"]
            for pos, d in node.history:
                grid[pos] = dmap[d]  # type: ignore
            grid[node.position] = "#"  # type: ignore
            draw_grid(grid)  # type: ignore
            return node.loss
        visited[key] = node.loss
        neighbours = around(node.position)

        # for e, d in enumerate([(node.direction - 1) % 4, node.direction, (node.direction + 1) % 4]):
        for d, neighbor in enumerate(neighbours):
            if node.chain == 3 or neighbor not in grid:
                continue

            if visited.get((neighbor, d), node.loss + 1) > node.loss:
                heapq.heappush(
                    queue,
                    Node(
                        node.loss + grid[neighbor],
                        neighbor,
                        d,
                        node.chain + 1 if node.direction == d else 1,
                        [*node.history, (node.position, node.direction)],
                    ),
                )

    return 0


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


def test_part_1() -> None:
    test_input = get_example_input()
    with time_limit(5):
        assert part_1(test_input) == 102


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


# @no_input_skip
# def test_part_1_real() -> None:
#    real_input = read_input(__file__)
#    with time_limit(10):
#        assert part_1(real_input) > 837


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    part_1(get_example_input())
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
