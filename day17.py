from typing import Tuple, List


def parse_input(task_input: str) -> Tuple[int, int, int, List[int]]:
    rega, regb, regc, _, prog = task_input.split('\n')
    a = int(rega.split(': ')[1])
    b = int(regb.split(': ')[1])
    c = int(regc.split(': ')[1])
    program = [int(x) for x in prog.split(': ')[1].split(',')]
    return a, b, c, program


def resolve_combo_operand(a: int, b: int, c: int, combo_operand: int) -> int:
    if 0 <= combo_operand <= 3:
        return combo_operand
    if combo_operand == 4:
        return a
    if combo_operand == 5:
        return b
    if combo_operand == 6:
        return c
    raise ValueError("Combo operand unsupported", combo_operand)


def execute_program(a: int, b: int, c: int, program: List[int]):
    output = []

    i = 0
    while i + 1 < len(program):
        instruction = program[i]
        operand = program[i + 1]

        match instruction:
            case 0:  # adv
                a = a // int(2 ** resolve_combo_operand(a, b, c, operand))
            case 1:  # bxl
                b ^= operand
            case 2:  # bst
                b = resolve_combo_operand(a, b, c, operand) % 8
            case 3:  # jnz
                if a != 0:
                    i = operand
                    continue  # do not increment instruction pointer
            case 4:  # bxc
                b ^= c
            case 5:  # out
                output.append(resolve_combo_operand(a, b, c, operand) % 8)
            case 6:  # bdv
                b = a // int(2 ** resolve_combo_operand(a, b, c, operand))
            case 7:  # cdv
                c = a // int(2 ** resolve_combo_operand(a, b, c, operand))
        i += 2

    return output


def part1(task_input: str):
    a, b, c, program = parse_input(task_input)
    output = execute_program(a, b, c, program)
    return ','.join(map(str, output))


"""
For part 2, I manually reverse-engineered (decompiled? lol) my task input.
This solution does not generalize to other task inputs. Because it can't.
So don't expect this to make any sense for YOUR program because it won't.
I'm a little sad because I love to write general solutions for general inputs, but some
tasks are just not designed for that.
Still, I do like this task!
"""


def my_program(a):
    # In simple pseudocode, my program is this:
    # :start
    # b = a % 8
    # b = b ^ 5
    # c = a // 2**b
    # b = b ^ 6
    # b = b ^ c
    # out.append(b % 8)
    # a = a // 8
    # if a != 0: goto start

    # Simplifying this further, the following is equivalent to my program (registers b and c not necessary at all)
    out = []
    while True:
        out.append((((a & 7) ^ 3) ^ (a >> ((a & 7) ^ 5))) & 7)
        a >>= 3
        if a == 0:
            return out


def part2(task_input: str):
    target_out = [2, 4, 1, 5, 7, 5, 1, 6, 4, 1, 5, 5, 0, 3, 3, 0]
    possible_as = [0]

    for i in range(len(target_out)-1, -1, -1):
        new_possible_as = []
        partial_output = target_out[i:]              # check if the last (n-i) digits are correct
        for a_prefix in possible_as:                 # if so, shift that a to the left and go on
            for suffix in range(8):                  # since in every step, a 3-bit number is appended to the result
                a = (a_prefix << 3) | suffix         # and a is shifted to the right by 3, we are bound to find
                if my_program(a) == partial_output:  # all possible as with the correct output this way.
                    new_possible_as.append(a)
        possible_as = new_possible_as

    return min(possible_as)
