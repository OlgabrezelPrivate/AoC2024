def part1(task_input: str):
    ways = [((1, 0), (2, 0), (3, 0)),
            ((-1, 0), (-2, 0), (-3, 0)),
            ((1, 1), (2, 2), (3, 3)),
            ((-1, -1), (-2, -2), (-3, -3)),
            ((0, 1), (0, 2), (0, 3)),
            ((0, -1), (0, -2), (0, -3)),
            ((1, -1), (2, -2), (3, -3)),
            ((-1, 1), (-2, 2), (-3, 3))]

    counter = 0
    lines = task_input.split('\n')
    rows = len(lines)
    cols = len(lines[0])
    for y in range(rows):
        for x in range(cols):
            if lines[y][x] == 'X':
                for ((x1, y1), (x2, y2), (x3, y3)) in ways:
                    if (0 <= x + x3 < cols) and \
                       (0 <= y + y3 < rows) and \
                       (lines[y + y1][x + x1] == 'M') and \
                       (lines[y + y2][x + x2] == 'A') and \
                       (lines[y + y3][x + x3] == 'S'):
                        counter += 1
    return counter


def part2(task_input: str):
    counter = 0
    lines = task_input.split('\n')
    rows = len(lines)
    cols = len(lines[0])

    for y in range(1, rows - 1):
        for x in range(1, cols - 1):
            if lines[y][x] == 'A':
                if ((lines[y-1][x-1] == 'M') and (lines[y+1][x+1] == 'S')) or \
                   ((lines[y-1][x-1] == 'S') and (lines[y+1][x+1] == 'M')):
                    if ((lines[y-1][x+1] == 'M') and (lines[y+1][x-1] == 'S')) or \
                       ((lines[y-1][x+1] == 'S') and (lines[y+1][x-1] == 'M')):
                        counter += 1
    return counter
