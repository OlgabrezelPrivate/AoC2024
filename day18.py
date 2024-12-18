from functools import total_ordering
from math import inf
from typing import Dict, Tuple
from heapq import heappop, heappush, _siftdown


@total_ordering
class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.edges = []
        self.dist = inf
        self.prev = []

    def __eq__(self, other):
        return isinstance(other, Node) and (self.x == other.x) and (self.y == other.y) and (self.dim == other.dim)

    def __lt__(self, other):
        return self.dist < other.dist


def dijkstra(nodes: Dict[Tuple[int, int], Node], sx: int, sy: int, ex: int, ey: int):
    """
    Shamelessly copied from day16.py
    A bit disappointed by this task. Just shortest paths again. :/
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
                    e.prev = u
                    _siftdown(Q, 0, Q.index(e))


def part1(task_input: str):
    MAX_COORDINATE = 70  # 6 for debug
    FALLING_BYTES = 1024  # 12 for debug

    positions = [(int(row.split(',')[0]), int(row.split(',')[1])) for row in task_input.split('\n')]
    corrupted = set(positions[:FALLING_BYTES])
    nodes = dict()

    for y in range(MAX_COORDINATE+1):
        for x in range(MAX_COORDINATE+1):
            if (x, y) not in corrupted:
                nodes[x, y] = Node(x, y)

    for y in range(MAX_COORDINATE+1):
        for x in range(MAX_COORDINATE+1):
            if (x, y) in nodes:
                for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    if (x+dx, y+dy) in nodes:
                        nodes[x, y].edges.append(nodes[x+dx, y+dy])

    dijkstra(nodes, 0, 0, MAX_COORDINATE, MAX_COORDINATE)
    return nodes[MAX_COORDINATE, MAX_COORDINATE].dist


def part2(task_input: str):
    print("This is absolutely not optimized and takes about 15:30 minutes.")
    print("Easiest optimization would be to perform a binary search on the positions")
    print("instead of the linear search I'm doing, but I can't be bothered.")
    MAX_COORDINATE = 70  # 6 for debug
    positions = [(int(row.split(',')[0]), int(row.split(',')[1])) for row in task_input.split('\n')]
    corrupted = set()
    nodes = dict()

    for y in range(MAX_COORDINATE+1):
        for x in range(MAX_COORDINATE+1):
            nodes[x, y] = Node(x, y)

    for y in range(MAX_COORDINATE+1):
        for x in range(MAX_COORDINATE+1):
            if (x, y) in nodes:
                for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    if (x+dx, y+dy) in nodes:
                        nodes[x, y].edges.append(nodes[x+dx, y+dy])

    i = len(positions)
    for p in positions:
        i -= 1
        print(i)
        corrupted.add(p)

        if p not in nodes:
            continue

        blocked_node = nodes[p]
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if (p[0]+dx, p[1]+dy) in nodes:
                nodes[p[0]+dx, p[1]+dy].edges.remove(blocked_node)

        del nodes[p]

        for x, y in nodes:
            nodes[x, y].dist = inf

        dijkstra(nodes, 0, 0, MAX_COORDINATE, MAX_COORDINATE)

        if nodes[MAX_COORDINATE, MAX_COORDINATE].dist == inf:
            return p
