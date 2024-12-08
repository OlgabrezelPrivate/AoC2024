from typing import Dict, List, Tuple


def parse_input(task_input: str) -> Tuple[List[List[str]], Dict[str, List[Tuple[int, int]]]]:
    grid = [list(x) for x in task_input.split('\n')]
    antennas = dict()

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != '.':
                a = grid[y][x]
                if a not in antennas:
                    antennas[a] = [(x, y)]
                else:
                    antennas[a].append((x, y))

    return grid, antennas


def part1(task_input: str):
    grid, antennas = parse_input(task_input)
    rows = len(grid)
    cols = len(grid[0])
    antinodes = set()

    for a in antennas:
        positions = antennas[a]
        for x1, y1 in positions:
            for x2, y2 in positions:
                if (x1 == x2) and (y1 == y2):
                    continue

                antinode1 = (2 * x1 - x2, 2 * y1 - y2)
                if (0 <= antinode1[0] < cols) and (0 <= antinode1[1] < rows):
                    antinodes.add(antinode1)

                antinode2 = (2 * x2 - x1, 2 * y2 - y1)
                if (0 <= antinode2[0] < cols) and (0 <= antinode2[1] < rows):
                    antinodes.add(antinode2)

    return len(antinodes)


def part2(task_input: str):
    grid, antennas = parse_input(task_input)
    rows = len(grid)
    cols = len(grid[0])
    antinodes = set()

    for a in antennas:
        positions = antennas[a]
        for x1, y1 in positions:
            for x2, y2 in positions:
                if (x1 == x2) and (y1 == y2):
                    continue

                dx = x2 - x1
                dy = y2 - y1

                x = x1
                y = y1
                while (0 <= x < cols) and (0 <= y < rows):
                    antinodes.add((x, y))
                    x -= dx
                    y -= dy

                x = x1
                y = y1
                while (0 <= x < cols) and (0 <= y < rows):
                    antinodes.add((x, y))
                    x += dx
                    y += dy

    return len(antinodes)
