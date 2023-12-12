GridType = dict[tuple[int, int], str]


def draw_grid(grid: GridType, missing: str = "."):
    width = set()
    height = set()
    for x, y in grid.keys():
        width.add(x)
        height.add(y)

    for y in range(min(height), max(height) + 1):
        for x in range(min(width), max(width) + 1):
            if (x, y) in grid:
                print(grid[x, y], end="")
            else:
                print(missing, end="")
        print()
