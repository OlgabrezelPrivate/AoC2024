from typing import Tuple, List


def parse_input(task_input: str, bigger_grid: bool) -> Tuple[List[List[str]], str, Tuple[int, int]]:
    grid_raw, instructions_raw = task_input.split('\n\n')

    if bigger_grid:
        grid_raw = grid_raw.replace('#', '##').replace('.', '..').replace('O', '[]').replace('@', '@.')

    grid = [list(row) for row in grid_raw.split('\n')]
    instructions = instructions_raw.replace('\n', '')
    robot_pos = None
    for y in range(len(grid)):
        if '@' in grid[y]:
            robot_pos = (grid[y].index('@'), y)
            break

    return grid, instructions, robot_pos


def part1(task_input: str):
    grid, instructions, (rx, ry) = parse_input(task_input, False)
    rows = len(grid)
    cols = len(grid[0])

    for ins in instructions:
        dx, dy = (
            (-1, 0) if ins == '<' else
            (0, -1) if ins == '^' else
            (1, 0) if ins == '>' else
            (0, 1)  # v
        )
        x, y = rx, ry
        while grid[y+dy][x+dx] == 'O':
            x += dx
            y += dy
        if grid[y+dy][x+dx] == '.':  # otherwise it must be '#' and nothing is being pushed
            if (x, y) != (rx, ry):  # at least one object is pushed
                grid[y+dy][x+dx] = 'O'
                grid[ry+dy][rx+dx] = '@'
                # move robot too
            else:                   # robot is moving without pushing
                grid[y+dy][x+dx] = '@'

            grid[ry][rx] = '.'
            rx += dx
            ry += dy

    res = 0
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 'O':
                res += 100 * y + x
    return res


def part2(task_input: str):
    grid, instructions, (rx, ry) = parse_input(task_input, True)
    rows = len(grid)
    cols = len(grid[0])

    for ins in instructions:
        dx, dy = (
            (-1, 0) if ins == '<' else
            (0, -1) if ins == '^' else
            (1, 0) if ins == '>' else
            (0, 1)  # v
        )
        all_pushing_positions = [(rx, ry)]
        pushing_positions_stack = [(rx, ry)]
        blocked = False

        while len(pushing_positions_stack):
            x, y = pushing_positions_stack.pop()
            if grid[y+dy][x+dx] == '[':
                if ins != '<':  # already pushing anyway, since the push must come from the corresponding ]
                    pushing_positions_stack.extend([(x+dx+1, y+dy), (x+dx, y+dy)])
                    all_pushing_positions.extend([(x+dx+1, y+dy), (x+dx, y+dy)])
            elif grid[y+dy][x+dx] == ']':
                if ins != '>':  # already pushing anyway, since the push must come from the corresponding [
                    pushing_positions_stack.extend([(x+dx, y+dy), (x+dx-1, y+dy)])
                    all_pushing_positions.extend([(x+dx, y+dy), (x+dx-1, y+dy)])
            elif grid[y+dy][x+dx] == '#':
                blocked = True
                break

        if blocked:
            continue

        new_grid = [row.copy() for row in grid]
        for x, y in all_pushing_positions:
            new_grid[y+dy][x+dx] = grid[y][x]
            if (x-dx, y-dy) not in all_pushing_positions:
                new_grid[y][x] = '.'
        new_grid[ry][rx] = '.'

        grid = new_grid
        rx += dx
        ry += dy

    res = 0
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == '[':
                res += 100 * y + x
    return res
