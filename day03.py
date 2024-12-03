import re


def part1(task_input: str):
    matches = re.findall(r'mul\((\d+),(\d+)\)', task_input)
    return sum(int(m[0]) * int(m[1]) for m in matches)


def part2(task_input: str):
    removed = re.sub(r"don't\(\)[\d\D]*?do\(\)", '', task_input)  # remove          `don't()` + <anything> + `do()`
    removed = re.sub(r"don't\(\)[\d\D]*", '', removed)            # remove trailing `don't()` + <anything>
    return part1(removed)
