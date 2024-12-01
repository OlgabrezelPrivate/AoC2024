def part1(task_input: str):
    lines = task_input.split('\n')
    left = sorted([int(x.split(' ')[0]) for x in lines])
    right = sorted([int(x.split(' ')[-1]) for x in lines])

    distance_sum = 0
    for le, ri in zip(left, right):
        distance_sum += abs(le - ri)

    return distance_sum


def part2(task_input: str):
    lines = task_input.split('\n')
    left = [int(x.split(' ')[0]) for x in lines]
    right = [int(x.split(' ')[-1]) for x in lines]

    similarity = 0
    for le in left:
        similarity += le * right.count(le)

    return similarity
