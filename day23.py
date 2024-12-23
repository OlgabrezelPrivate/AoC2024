from typing import Set, Dict
from collections import defaultdict


def parse_input(task_input: str) -> Dict[str, Set[str]]:
    connections_raw = [tuple(row.split('-')) for row in task_input.split('\n')]
    connections = defaultdict(set)

    for a, b in connections_raw:
        connections[a].add(b)
        connections[b].add(a)
    return connections


def part1(task_input: str):
    connections = parse_input(task_input)
    sets = set()

    for name1 in connections:
        if name1.startswith('t'):
            for name2 in connections[name1]:
                for name3 in connections[name2]:
                    if name1 in connections[name3]:
                        sets.add(tuple(sorted([name1, name2, name3])))
    return len(sets)


def part2(task_input: str):
    print("This takes approximately 15 seconds...")
    connections = parse_input(task_input)

    cur_comps = set()
    for name1 in connections:
        for name2 in connections[name1]:
            cur_comps.add(tuple(sorted([name1, name2])))  # all pairwise-connected components of length 2 (aka edges)

    while True:  # now go from pairwise-connected components of length k to length k+1 until there's only 1 left.
        if len(cur_comps) == 1:
            return ','.join(next(iter(cur_comps)))

        new_comps = set()
        for comp in cur_comps:
            for new_name in connections:
                if new_name not in comp:
                    for existing_name in comp:
                        if existing_name not in connections[new_name]:
                            break
                    else:
                        new_comps.add(tuple(sorted([new_name, *comp])))
        cur_comps = new_comps
