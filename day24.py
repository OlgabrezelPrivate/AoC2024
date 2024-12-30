from typing import Dict, Tuple
from collections import defaultdict


def parse_input(task_input: str) -> Tuple[Dict[str, bool], Dict[str, Tuple[str, str, str]]]:
    states_raw, wires_raw = task_input.split('\n\n')

    states = defaultdict(lambda: False)
    for state in states_raw.split('\n'):
        name, val = state.split(': ')
        states[name] = bool(int(val))

    wires = dict()
    for wire in wires_raw.split('\n'):
        in1, op, in2, _, out = wire.split(' ')
        wires[out] = (op, in1, in2)

    return states, wires


def run_machine(states: Dict[str, bool], wires: Dict[str, Tuple[str, str, str]]):
    """Runs the machine until it doesn't change anymore, updating `states`."""
    changed = True
    while changed:
        changed = False
        for out, (op, in1, in2) in wires.items():
            if op == 'AND':
                new = states[in1] and states[in2]
            elif op == 'OR':
                new = states[in1] or states[in2]
            else:  # 'XOR'
                new = states[in1] != states[in2]

            if (out not in states) or (states[out] != new):
                states[out] = new
                changed = True


def get_number(states: Dict[str, bool], prefix: str) -> int:
    i = 0
    result = 0

    while (bitname := f'{prefix}{str(i).rjust(2, "0")}') in states:
        result |= int(states[bitname]) << i
        i += 1
    return result


def part1(task_input: str):
    states, wires = parse_input(task_input)
    run_machine(states, wires)
    return get_number(states, 'z')


def part2(task_input: str):
    '''
    First I thought I need to check all possible swaps (too expensive) or build the whole adder from scratch
    (but not sure how that would reveal the necessary swaps).
    But turns out, you don't even need to care about the swaps. Just check for all nodes that are wired wrongly and
    put them in alphabetical order. The fact that pairwise swaps of them could fix the adder isn't even relevant
    to this solution.
    Credits to https://blog.lojic.com/2024/12/29/advent-of-code-2024-day-24-crossed-wires.html for the idea
    (I stole the code. Funnily enough, I had already represented the parsed wires exactly the same way as this blogger,
    so this was really just copy-pasting the entire for-loop).
    '''
    _, wires = parse_input(task_input)

    connections = wires.items()
    wrong = set()

    for out, (op, w1, w2) in connections:
        if out[0] == 'z' and op != 'XOR' and out != 'z45':
            wrong.add(out)

        if op == 'XOR' and \
           out[0] not in ('x', 'y', 'z') and \
           w1[0] not in ('x', 'y', 'z') and \
           w2[0] not in ('x', 'y', 'z'):
            wrong.add(out)

        if op == 'AND' and 'x00' not in (w1, w2):
            for out2, (op2, w1_2, w2_2) in connections:
                if (out == w1_2 or out == w2_2) and op2 != 'OR':
                    wrong.add(out)

        if op == 'XOR':
            for out2, (op2, w1_2, w2_2) in connections:
                if (out == w1_2 or out == w2_2) and op2 == 'OR':
                    wrong.add(out)

    return ','.join(sorted(wrong))


"""
OLD ATTEMPTS HERE

from random import randint
from functools import cache

@cache
def trace_inputs(out: str):
    global wires
    inputs = defaultdict(lambda: 0)
    _, in1, in2 = wires[out]

    if in1.startswith('x') or in1.startswith('y'):
        inputs[in1] += 1
    else:
        for inp, val in trace_inputs(in1).items():
            inputs[inp] += val

    if in1.startswith('x') or in1.startswith('y'):
        inputs[in2] += 1
    else:
        for inp, val in trace_inputs(in2).items():
            inputs[inp] += val

    return inputs


def part2_attempt2(task_input: str):
    global wires
    _, wires = parse_input(task_input)
    suspects = set()

    for out in sorted(wires.keys()):
        if out.startswith('z'):
            k = int(out[1:])

            inputs = dict(trace_inputs(out))
            should_inputs = ({'x00': 1, 'y00': 1, f'x{str(k).rjust(2, "0")}': 1, f'y{str(k).rjust(2, "0")}': 1} |
                             {f'x{str(i).rjust(2, "0")}': 2 for i in range(1, k)} |
                             {f'y{str(i).rjust(2, "0")}': 2 for i in range(1, k)})

            if inputs != should_inputs:
                suspects.add(out)
                print(out, inputs, len(inputs))
                print('')


def part2_attempt1(task_input: str):
    states, wires = parse_input(task_input)
    suspects = set()

    for i in range(100):
        for k in range(45):
            states[f'x{str(k).rjust(2, "0")}'] = randint(0, 1) == 1
            states[f'y{str(k).rjust(2, "0")}'] = randint(0, 1) == 1

        x = get_number(states, 'x')
        y = get_number(states, 'y')
        run_machine(states, wires)

        for k in range(44):
            x_bit = int(states[f'x{str(k).rjust(2, "0")}'])
            y_bit = int(states[f'y{str(k).rjust(2, "0")}'])
            z_bit = int(states[f'z{str(k).rjust(2, "0")}'])

            bitmask = (1 << k) - 1
            carry = int(bool(((x & bitmask) + (y & bitmask)) & (1 << k)))

            if (x_bit + y_bit + carry) & 1 != z_bit:
                suspects.add(k)

    return sorted(suspects)
"""
