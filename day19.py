from typing import List, Tuple
from functools import cache


def parse_input(task_input: str) -> Tuple[Tuple[str, ...], List[str]]:
    towels_raw, designs_raw = task_input.split('\n\n')
    towels = tuple(towels_raw.split(', '))
    designs = designs_raw.split('\n')
    return towels, designs


def can_arrange(design: str, towels: Tuple[str, ...]) -> bool:
    if len(design) == 0:
        return True

    for t in towels:
        if design.startswith(t) and can_arrange(design[len(t):], towels):
            return True
    return False


def part1(task_input: str):
    towels, designs = parse_input(task_input)
    return len([d for d in designs if can_arrange(d, towels)])


@cache
def count_arrangements(design: str, towels: Tuple[str, ...]) -> bool:
    if len(design) == 0:
        return 1

    count = 0
    for t in towels:
        if design.startswith(t):
            count += count_arrangements(design[len(t):], towels)
    return count


def part2(task_input: str):
    towels, designs = parse_input(task_input)
    return sum(count_arrangements(d, towels) for d in designs)
