from typing import List, Tuple


def parse_input(task_input: str) -> Tuple[List[List[int]], List[List[int]]]:
    sec1, sec2 = task_input.split('\n\n')
    orders = [list(map(int, x.split('|'))) for x in sec1.split('\n')]
    updates = [list(map(int, x.split(','))) for x in sec2.split('\n')]
    return orders, updates


def is_allowed(update, orders):
    for early, late in orders:
        if (early in update) and (late in update) and update.index(early) > update.index(late):
            return False
    return True


def part1(task_input: str):
    orders, updates = parse_input(task_input)
    res = 0
    for u in updates:
        if is_allowed(u, orders):
            res += u[len(u) // 2]
    return res


def part2(task_input: str):
    orders, updates = parse_input(task_input)
    wrong_updates = [x for x in updates if not is_allowed(x, orders)]
    res = 0
    for i in range(len(wrong_updates)):
        u = wrong_updates[i].copy()
        relevant_orders = [(early, late) for early, late in orders if (early in u) and (late in u)]
        correct_order = [u.pop()]
        while len(u):
            nxt = u.pop()
            for j in range(len(correct_order) + 1):
                trial = correct_order.copy()
                trial.insert(j, nxt)
                if is_allowed(trial, relevant_orders):
                    correct_order = trial
                    break
        res += correct_order[len(correct_order) // 2]
    return res
