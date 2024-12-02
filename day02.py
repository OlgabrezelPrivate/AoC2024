def is_safe(r: list):
    increasing = None
    for i in range(len(r) - 1):
        if (r[i] == r[i + 1]) or (r[i] < r[i + 1] - 3) or (r[i] > r[i + 1] + 3):
            return False
        now_increasing = r[i] < r[i + 1]
        if increasing is None:
            increasing = now_increasing
        if increasing != now_increasing:
            return False
    return True


def part1(task_input: str):
    reports = [list(map(int, row.split(' '))) for row in task_input.split('\n')]
    return len(list(filter(is_safe, reports)))


def part2(task_input: str):
    reports = [list(map(int, row.split(' '))) for row in task_input.split('\n')]
    safe = 0
    for r in reports:
        for pos in range(len(r)):
            r_new = r[:pos] + r[pos + 1:]  # remove the element at position `pos`
            if is_safe(r_new):
                safe += 1
                break
    return safe
