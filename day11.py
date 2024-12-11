from math import log10
from typing import Dict


def blink(stones: Dict[int, int]) -> Dict[int, int]:
    new_stones = dict()
    for s in stones:
        if s == 0:
            if 1 not in new_stones:
                new_stones[1] = 0
            new_stones[1] += stones[s]
        elif (digits := int(log10(s)) + 1) % 2 == 0:
            mod = 10**(digits // 2)
            s1 = s // mod
            s2 = s % mod
            if s1 not in new_stones:
                new_stones[s1] = 0
            if s2 not in new_stones:
                new_stones[s2] = 0
            new_stones[s1] += stones[s]
            new_stones[s2] += stones[s]
        else:
            if s * 2024 not in new_stones:
                new_stones[s * 2024] = 0
            new_stones[s * 2024] += stones[s]
    return new_stones


def num_stones_after_n_blinks(n: int, task_input: str):
    stones_raw = [int(x) for x in task_input.split(' ')]
    stones = {s: stones_raw.count(s) for s in set(stones_raw)}
    for i in range(n):
        stones = blink(stones)
    return sum(stones.values())


def part1(task_input: str):
    return num_stones_after_n_blinks(25, task_input)


def part2(task_input: str):
    return num_stones_after_n_blinks(75, task_input)
