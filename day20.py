from typing import Tuple, Dict
from heapq import heappop, heappush, _siftdown
from functools import total_ordering
from math import inf


@total_ordering
class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.edges = []
        self.dist = inf

    def __eq__(self, other):
        return isinstance(other, Node) and (self.x == other.x) and (self.y == other.y)

    def __lt__(self, other):
        return self.dist < other.dist


def parse_input(task_input: str) -> Tuple[Dict[Tuple[int, int], Node], Tuple[int, int], Tuple[int, int]]:
    grid = [list(row) for row in task_input.split('\n')]
    rows = len(grid)
    cols = len(grid[0])
    start = None
    end = None
    nodes = dict()

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 'S':
                start = (x, y)
                grid[y][x] = '.'
            if grid[y][x] == 'E':
                end = (x, y)
                grid[y][x] = '.'

            if grid[y][x] == '.':
                nodes[x, y] = Node(x, y)

    for y in range(rows):
        for x in range(cols):
            for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                if ((x, y) in nodes) and ((x+dx, y+dy) in nodes):
                    nodes[x, y].edges.append(nodes[x+dx, y+dy])
    return nodes, start, end


def dijkstra(nodes: Dict[Tuple[int, int], Node], sx: int, sy: int, ex: int, ey: int):
    """
    Since there is only one path, dijkstra is not really needed here, but it was too late when I realised that.
    So I just copied the implementation from days 16 and 18 again.
    """
    Q = []
    enqueued = set()

    nodes[sx, sy].dist = 0
    for n in nodes.values():
        heappush(Q, n)
        enqueued.add((n.x, n.y))

    while len(Q):
        u = heappop(Q)
        enqueued.remove((u.x, u.y))
        for e in u.edges:
            if (e.x, e.y) in enqueued:
                new_dist = u.dist + 1
                if new_dist < e.dist:
                    e.dist = new_dist
                    _siftdown(Q, 0, Q.index(e))


def number_of_cheats_better_than_100ps(task_input: str, max_cheat_length: int) -> int:
    nodes, (sx, sy), (ex, ey) = parse_input(task_input)
    dijkstra(nodes, sx, sy, ex, ey)
    result = 0

    for x, y in nodes:
        for dx in range(-max_cheat_length, max_cheat_length+1):
            max_dy = max_cheat_length - abs(dx)
            for dy in range(-max_dy, max_dy+1):
                if (x+dx, y+dy) in nodes:
                    time_save = nodes[x+dx, y+dy].dist - nodes[x, y].dist - abs(dx) - abs(dy)

                    if time_save >= 100:
                        result += 1

    return result


def part1(task_input: str):
    return number_of_cheats_better_than_100ps(task_input, 2)


def part2(task_input: str):
    return number_of_cheats_better_than_100ps(task_input, 20)
