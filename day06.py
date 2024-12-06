from typing import List, Tuple, Optional, Set


def get_guard_pos_direction(grid: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Get the guard's initial position and direction facing.
    """
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] not in ['.', '#']:  # This is the starting position!
                pos = (x, y)
                direction = (
                    (0, -1) if grid[y][x] == '^' else
                    (1, 0) if grid[y][x] == '>' else
                    (0, 1) if grid[y][x] == 'v' else
                    (-1, 0)
                )
                return pos, direction


def guard_walk(grid: List[List[str]],
               pos: Tuple[int, int],
               direction: Tuple[int, int]) -> Optional[Set[Tuple[int, int]]]:
    """
    Simulate the guard's walk, depending on the grid, their initial position and direction.

    Returns:
        The set of all visited positions of the guard, or None if the guard gets stuck in a loop.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited_squares = set()
    visited_squares_with_direction = set()

    while True:
        if (pos, direction) in visited_squares_with_direction:  # we've been here before, endless loop
            return None

        visited_squares.add(pos)
        visited_squares_with_direction.add((pos, direction))

        next_square = (pos[0] + direction[0], pos[1] + direction[1])
        if not ((0 <= next_square[0] < cols) and (0 <= next_square[1] < rows)):
            return visited_squares  # next step will lead the guard off the map

        if grid[next_square[1]][next_square[0]] == '#':  # turn right
            direction = (
                (1, 0) if direction == (0, -1) else
                (0, 1) if direction == (1, 0) else
                (-1, 0) if direction == (0, 1) else
                (0, -1)
            )
        else:                                            # move forward
            pos = next_square


def part1(task_input: str):
    grid = [list(x) for x in task_input.split('\n')]
    pos, direction = get_guard_pos_direction(grid)
    visited = guard_walk(grid, pos, direction)
    return len(visited)


def part2(task_input: str):
    print("This takes approximately 7 seconds...")

    grid = [list(x) for x in task_input.split('\n')]
    pos, direction = get_guard_pos_direction(grid)

    res = 0
    potential_squares = guard_walk(grid, pos, direction) - {pos}  # only visited squares can be potential obstacle positions
    for sq in potential_squares:
        grid[sq[1]][sq[0]] = '#'
        if guard_walk(grid, pos, direction) is None:  # we got stuck in a loop with this grid modification
            res += 1
        grid[sq[1]][sq[0]] = '.'
    return res
