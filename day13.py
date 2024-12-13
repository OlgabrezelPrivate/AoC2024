def parse_input(task_input: str, unit_conversion_error: bool):
    machines = []
    machines_raw = task_input.split('\n\n')
    for m in machines_raw:
        rows = [x.split(': ')[1].split(', ') for x in m.split('\n')]
        ax = int(rows[0][0][2:])
        ay = int(rows[0][1][2:])
        bx = int(rows[1][0][2:])
        by = int(rows[1][1][2:])
        px = int(rows[2][0][2:])
        py = int(rows[2][1][2:])
        if not unit_conversion_error:
            px += 10000000000000
            py += 10000000000000
        machines.append((ax, ay, bx, by, px, py))
    return machines


def part1(task_input: str):  # naive approach as intended by the task :)
    machines = parse_input(task_input, True)
    tokens_spent = 0

    for ax, ay, bx, by, px, py in machines:
        price_possibilities = set()
        for a_presses in range(100):
            if (a_presses * ax > px) or (a_presses * ay > py):
                continue
            for b_presses in range(100):
                x = a_presses * ax + b_presses * bx
                y = a_presses * ay + b_presses * by
                if (x > px) or (y > py):
                    continue
                if (x == px) and (y == py):
                    price_possibilities.add((a_presses, b_presses))
        if len(price_possibilities):
            a, b = sorted(price_possibilities, key=lambda x: 3 * x[0] + x[1])[0]
            tokens_spent += 3 * a + b

    return tokens_spent


def part2(task_input: str):  # the whole thing is really just a system of linear equations
    machines = parse_input(task_input, False)
    tokens_spent = 0

    for ax, ay, bx, by, px, py in machines:
        # a * ax + b * bx = px
        # a * ay + b * by = py

        # (px - b * bx) / ax = a = (py - b * by) / ay

        # (px - b * bx) * ay = (py - b * by) * ax

        # px * ay - b * bx * ay = py * ax - b * by * ax

        # b * by * ax - b * bx * ay = py * ax - px * ay

        # b * (by * ax - bx * ay) = py * ax - px * ay

        b = (py * ax - px * ay) / (by * ax - bx * ay)
        a = (py - b * by) / ay
        if a.is_integer() and b.is_integer():  # otherwise there is no real-world solution
            tokens_spent += 3 * int(a) + int(b)

    return tokens_spent
