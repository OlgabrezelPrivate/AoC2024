from typing import List, Set, Tuple


def dfs(grid: List[List[str]], visited: Set[Tuple[int, int]], x: int, y: int, rows: int, cols: int):
    """
    Depth-First Search to find all squares belonging to the current grid. The set `visited` is mutated and
    contains all squares belonging to the current square's region after the function call is finished.
    """
    visited.add((x, y))
    plant = grid[y][x]

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (0 <= x+dx < cols) and (0 <= y+dy < rows) and ((x+dx, y+dy) not in visited) and (grid[y+dy][x+dx] == plant):
            dfs(grid, visited, x+dx, y+dy, rows, cols)


def get_regions(task_input: str) -> Set[Tuple[int, int]]:
    grid = [list(row) for row in task_input.split('\n')]
    rows = len(grid)
    cols = len(grid[0])

    all_visited = set()
    regions = []
    for y in range(rows):
        for x in range(cols):
            if ((x, y) not in all_visited):
                visited = set()
                dfs(grid, visited, x, y, rows, cols)
                all_visited |= visited
                regions.append(visited)
    return regions


def get_perimeter(region: Set[Tuple[int, int]], sides_as_one: bool) -> int:
    perimeter = 0
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # in clockwise order

    for x, y in region:
        for i, (dx, dy) in enumerate(directions):
            if (x+dx, y+dy) not in region:
                delta_x, delta_y = directions[i-1]

                if ((not sides_as_one) or                              # For part 1, count all edges, always.
                   ((x + delta_x, y + delta_y) not in region) or       # For part 2, only count if this is the clockwise-first
                   ((x + delta_x + dx, y + delta_y + dy) in region)):  # square to have a border in direction (dx, dy)!
                    perimeter += 1
    return perimeter


def part1(task_input: str):
    return sum(len(r) * get_perimeter(r, False) for r in get_regions(task_input))


def part2(task_input: str):
    return sum(len(r) * get_perimeter(r, True) for r in get_regions(task_input))
