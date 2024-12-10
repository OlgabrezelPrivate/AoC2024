def get_trailheads(grid):
    rows = len(grid)
    cols = len(grid[0])
    trailheads = []
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 0:
                trailheads.append((x, y))
    return trailheads


def get_reachable_tops(grid, x, y):
    rows = len(grid)
    cols = len(grid[0])
    reachable = set()

    for dx, dy in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
        if (0 <= x + dx < cols) and (0 <= y + dy < rows) and (grid[y+dy][x+dx] == grid[y][x] + 1):
            if grid[y+dy][x+dx] == 9:
                reachable.add((x+dx, y+dy))
            else:
                reachable |= get_reachable_tops(grid, x+dx, y+dy)
    return reachable


def part1(task_input: str):
    grid = [list(map(int, row)) for row in task_input.split('\n')]
    trailheads = get_trailheads(grid)
    return sum(len(get_reachable_tops(grid, x, y)) for x, y in trailheads)


def get_rating(grid, x, y):
    rows = len(grid)
    cols = len(grid[0])
    rating = 0

    for dx, dy in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
        if (0 <= x + dx < cols) and (0 <= y + dy < rows) and (grid[y+dy][x+dx] == grid[y][x] + 1):
            if grid[y+dy][x+dx] == 9:
                rating += 1
            else:
                rating += get_rating(grid, x+dx, y+dy)
    return rating


def part2(task_input: str):
    grid = [list(map(int, row)) for row in task_input.split('\n')]
    trailheads = get_trailheads(grid)
    return sum(get_rating(grid, x, y) for x, y in trailheads)
