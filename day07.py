from typing import List, Tuple
from functools import cache
from math import log10


def parse_input(task_input: str) -> List[Tuple[int, Tuple[int, ...]]]:
    instructions = [(int(x.split(': ')[0]), tuple(int(y) for y in x.split(': ')[1].split(' ')))
                    for x in task_input.split('\n')]
    return instructions


@cache
def check1(result, actual, nums) -> bool:
    if len(nums) == 0:
        return result == actual
    return (
        check1(result, actual + nums[0], nums[1:]) or
        check1(result, actual * nums[0], nums[1:])
    )


def part1(task_input: str):
    instructions = parse_input(task_input)
    return sum(result for result, numbers in instructions
               if check1(result, numbers[0], numbers[1:]))


@cache
def check2(result, actual, nums) -> bool:
    if len(nums) == 0:
        return result == actual
    return (
        check2(result, actual + nums[0], nums[1:]) or
        check2(result, actual * nums[0], nums[1:]) or
        check2(result, actual * 10**int(log10(nums[0])+1) + nums[0], nums[1:])
    )


def part2(task_input: str):
    print("This takes approximately 26 seconds...")

    instructions = parse_input(task_input)
    return sum(result for result, numbers in instructions
               if check2(result, numbers[0], numbers[1:]))
