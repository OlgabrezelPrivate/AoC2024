from functools import cache
from math import inf


NUMERIC_KEYPAD = (('7',  '8', '9'),
                  ('4',  '5', '6'),
                  ('1',  '2', '3'),
                  (None, '0', 'A'))

NUM2POS = {num: (x, y) for y, row in enumerate(NUMERIC_KEYPAD) for x, num in enumerate(row) if num is not None}

DIRECTIONAL_KEYPAD = ((None, '^', 'A'),
                      ('<',  'v', '>'))

DIR2POS = {direc: (x, y) for y, row in enumerate(DIRECTIONAL_KEYPAD) for x, direc in enumerate(row) if direc is not None}


@cache
def get_sequences_to(cx, cy, input_keypad, x, y):
    if (x, y) == (cx, cy):
        return {''}

    result = set()

    if (x < cx) and input_keypad[y][x+1] is not None:
        options = get_sequences_to(cx, cy, input_keypad, x+1, y)
        result |= {f'>{o}' for o in options}
    if (x > cx) and input_keypad[y][x-1] is not None:
        options = get_sequences_to(cx, cy, input_keypad, x-1, y)
        result |= {f'<{o}' for o in options}
    if (y < cy) and input_keypad[y+1][x] is not None:
        options = get_sequences_to(cx, cy, input_keypad, x, y+1)
        result |= {f'v{o}' for o in options}
    if (y > cy) and input_keypad[y-1][x] is not None:
        options = get_sequences_to(cx, cy, input_keypad, x, y-1)
        result |= {f'^{o}' for o in options}

    return result


def get_cost_matrix_directional(num_directional_robots: int):
    cost_matrix = dict()
    for sy in range(2):
        for sx in range(3):
            if DIRECTIONAL_KEYPAD[sy][sx] is None:
                continue
            for ey in range(2):
                for ex in range(3):
                    if DIRECTIONAL_KEYPAD[ey][ex] is None:
                        continue

                    cost_matrix[sx, sy, ex, ey] = abs(sx-ex) + abs(sy-ey) + 1

    for iteration in range(num_directional_robots - 1):
        cost_matrix_new = dict()
        for sx, sy, ex, ey in cost_matrix:
            cost = inf
            sequences = get_sequences_to(ex, ey, DIRECTIONAL_KEYPAD, sx, sy)
            for seq in sequences:
                seq += 'A'
                seq_cost = cost_matrix[2, 0, *DIR2POS[seq[0]]]
                for i in range(len(seq)-1):
                    seq_cost += cost_matrix[*DIR2POS[seq[i]], *DIR2POS[seq[i+1]]]
                cost = min(cost, seq_cost)

            cost_matrix_new[sx, sy, ex, ey] = cost
        cost_matrix = cost_matrix_new

    return cost_matrix


def get_cost_matrix_numeric(cost_matrix_directional):
    cost_matrix = dict()
    for sy in range(4):
        for sx in range(3):
            if NUMERIC_KEYPAD[sy][sx] is None:
                continue
            for ey in range(4):
                for ex in range(3):
                    if NUMERIC_KEYPAD[ey][ex] is None:
                        continue

                    cost = inf
                    sequences = get_sequences_to(ex, ey, NUMERIC_KEYPAD, sx, sy)
                    for seq in sequences:
                        seq += 'A'
                        seq_cost = cost_matrix_directional[2, 0, *DIR2POS[seq[0]]]
                        for i in range(len(seq)-1):
                            seq_cost += cost_matrix_directional[*DIR2POS[seq[i]], *DIR2POS[seq[i+1]]]
                        cost = min(cost, seq_cost)

                    cost_matrix[sx, sy, ex, ey] = cost

    return cost_matrix


def get_num_button_presses(task_input: str, num_directional_robots: int):
    codes = task_input.split('\n')
    result = 0

    cost_matrix_directional = get_cost_matrix_directional(num_directional_robots)
    cost_matrix_numeric = get_cost_matrix_numeric(cost_matrix_directional)

    for code in codes:
        cost = cost_matrix_numeric[2, 3, *NUM2POS[code[0]]]
        for i in range(len(code)-1):
            cost += cost_matrix_numeric[*NUM2POS[code[i]], *NUM2POS[code[i+1]]]
        result += int(code[:-1]) * cost

    return result


def part1(task_input: str):
    return get_num_button_presses(task_input, 2)


def part2(task_input: str):
    return get_num_button_presses(task_input, 25)
