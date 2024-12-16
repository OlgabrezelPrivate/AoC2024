from typing import Dict, Tuple
from enum import IntEnum
from heapq import heappush, heappop, _siftdown
from math import inf
from functools import total_ordering


class Dimension(IntEnum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


@total_ordering
class Node:
    def __init__(self, x: int, y: int, dim: Dimension):
        self.x = x
        self.y = y
        self.dim = dim
        self.edges = []
        self.dist = inf
        self.prev = []

    def __eq__(self, other):
        return isinstance(other, Node) and (self.x == other.x) and (self.y == other.y) and (self.dim == other.dim)

    def __lt__(self, other):
        return self.dist < other.dist


class Edge:
    def __init__(self, to_node: Node, weight: int):
        self.to_node = to_node
        self.weight = weight


def parse_input(task_input: str) -> Tuple[Dict[Tuple[int, int, Dimension], Node], Tuple[int, int], Tuple[int, int]]:
    grid = [list(row) for row in task_input.split('\n')]
    rows = len(grid)
    cols = len(grid[0])

    nodes = dict()
    start = None
    end = None

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 'S':
                grid[y][x] = '.'
                start = (x, y)
            if grid[y][x] == 'E':
                grid[y][x] = '.'
                end = (x, y)

            if grid[y][x] == '.':
                nodes[x, y, Dimension.Up] = Node(x, y, Dimension.Up)
                nodes[x, y, Dimension.Right] = Node(x, y, Dimension.Right)
                nodes[x, y, Dimension.Down] = Node(x, y, Dimension.Down)
                nodes[x, y, Dimension.Left] = Node(x, y, Dimension.Left)

    for y in range(rows):
        for x in range(cols):
            if (x, y, Dimension.Up) in nodes:
                nodes[x, y, Dimension.Up].edges.extend([Edge(nodes[x, y, Dimension.Left], 1000),
                                                        Edge(nodes[x, y, Dimension.Right], 1000)])
                nodes[x, y, Dimension.Right].edges.extend([Edge(nodes[x, y, Dimension.Up], 1000),
                                                           Edge(nodes[x, y, Dimension.Down], 1000)])
                nodes[x, y, Dimension.Down].edges.extend([Edge(nodes[x, y, Dimension.Left], 1000),
                                                          Edge(nodes[x, y, Dimension.Right], 1000)])
                nodes[x, y, Dimension.Left].edges.extend([Edge(nodes[x, y, Dimension.Up], 1000),
                                                          Edge(nodes[x, y, Dimension.Down], 1000)])

            if ((x, y, Dimension.Up) in nodes) and ((x, y+1, Dimension.Up) in nodes):
                nodes[x, y+1, Dimension.Up].edges.append(Edge(nodes[x, y, Dimension.Up], 1))
            if ((x, y, Dimension.Right) in nodes) and ((x-1, y, Dimension.Right) in nodes):
                nodes[x-1, y, Dimension.Right].edges.append(Edge(nodes[x, y, Dimension.Right], 1))
            if ((x, y, Dimension.Down) in nodes) and ((x, y-1, Dimension.Down) in nodes):
                nodes[x, y-1, Dimension.Down].edges.append(Edge(nodes[x, y, Dimension.Down], 1))
            if ((x, y, Dimension.Left) in nodes) and ((x+1, y, Dimension.Left) in nodes):
                nodes[x+1, y, Dimension.Left].edges.append(Edge(nodes[x, y, Dimension.Left], 1))

    return nodes, start, end


def dijkstra(nodes: Dict[Tuple[int, int, Dimension], Node], sx: int, sy: int, sdim: Dimension, ex: int, ey: int):
    Q = []
    enqueued = set()

    nodes[sx, sy, sdim].dist = 0
    for n in nodes.values():
        heappush(Q, n)
        enqueued.add((n.x, n.y, n.dim))

    while len(Q):
        u = heappop(Q)
        enqueued.remove((u.x, u.y, u.dim))
        for e in u.edges:
            if (e.to_node.x, e.to_node.y, e.to_node.dim) in enqueued:
                new_dist = u.dist + e.weight
                if new_dist < e.to_node.dist:
                    e.to_node.dist = new_dist
                    e.to_node.prev = [u]
                    _siftdown(Q, 0, Q.index(e.to_node))
                elif new_dist == e.to_node.dist:
                    e.to_node.prev.append(u)


nodes: Dict[Tuple[int, int, Dimension], Node]
sx: int
sy: int
ex: int
ey: int


def part1(task_input: str):
    global nodes, sx, sy, ex, ey
    print('This takes approximately 31 seconds...')

    nodes, (sx, sy), (ex, ey) = parse_input(task_input)
    sdim = Dimension.Right  # start facing east
    dijkstra(nodes, sx, sy, sdim, ex, ey)
    return min(nodes[ex, ey, dim].dist for dim in [Dimension.Up, Dimension.Right, Dimension.Down, Dimension.Left])


def part2(task_input: str):
    global nodes, sx, sy, ex, ey
    print('This finishes immediately because we are reusing the dijkstra run from part 1!')

    edim = sorted(nodes[ex, ey, dim] for dim in [Dimension.Up, Dimension.Right, Dimension.Down, Dimension.Left])[0].dim
    good_tiles = set()
    way_stack = [nodes[ex, ey, edim]]

    while len(way_stack):
        n = way_stack.pop()
        good_tiles.add((n.x, n.y))
        for p in n.prev:
            way_stack.append(p)

    return len(good_tiles)
