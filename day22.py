from collections import defaultdict


def next_secret(secret: int):
    secret = ((secret << 6) ^ secret) & 0xFFFFFF
    secret = (secret >> 5) ^ secret
    return ((secret << 11) ^ secret) & 0xFFFFFF


def part1(task_input: str):
    buyers = [int(x) for x in task_input.split('\n')]
    result = 0

    for i in range(len(buyers)):
        secret = buyers[i]
        for j in range(2000):
            secret = next_secret(secret)
        result += secret
    return result


def part2(task_input: str):
    buyers = [int(x) for x in task_input.split('\n')]
    revenues = defaultdict(lambda: 0)

    for secret in buyers:
        seen = set()
        price4, price3, price2, price1, price0 = None, None, None, None, None

        for i in range(2001):
            price4 = price3
            price3 = price2
            price2 = price1
            price1 = price0
            price0 = secret % 10
            secret = next_secret(secret)
            if (i < 4):
                continue

            dif3 = price3 - price4
            dif2 = price2 - price3
            dif1 = price1 - price2
            dif0 = price0 - price1

            if ((dif3, dif2, dif1, dif0) in seen):
                continue

            seen.add((dif3, dif2, dif1, dif0))
            revenues[dif3, dif2, dif1, dif0] += price0

    return max(revenues.values())
