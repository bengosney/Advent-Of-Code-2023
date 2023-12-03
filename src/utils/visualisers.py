GridType = dict[tuple[int, int], str]


def draw_grid(grid: GridType, missing: str = "."):
    width = set()
    height = set()
    for x, y in grid.keys():
        width.add(x)
        height.add(y)

    for y in range(min(height), max(height)):
        for x in range(min(width), max(width)):
            print(grid[x, y], end="")
        print()
