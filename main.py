import argparse
import importlib
import os
import re
import time


def parse_args_and_get_day():
    parser = argparse.ArgumentParser(description="Ludwig's Advent of Code 2024 scripts. Runs the newest task by default. "
                                                 "You can pass a number to select which day's task to run instead.")
    parser.add_argument('day', metavar="DAY", type=int, nargs='?', help="Which day's task to run")
    args = parser.parse_args()

    if args.day:
        day = args.day
    else:
        days = [re.match(r'^day(\d\d).py$', d) for d in os.listdir('.')]
        day = max([int(m.group(1)) for m in days if m])

    return str(day).rjust(2, '0')


def read_input(day):
    file_name = f'input{day}.txt'

    if os.path.exists(file_name):
        with open(f'input{day}.txt', 'r') as file:
            return file.read()

    print(f'{file_name} not found. Please enter the task input, and finish with an empty line.')
    rows = []
    while row := input():
        rows.append(row)

    task_input = '\n'.join(rows)

    with open(file_name, 'w') as file:
        file.write(task_input)

    return task_input


def main():
    DAY = parse_args_and_get_day()

    module_name = f'day{DAY}'
    module = importlib.import_module(module_name)

    task_input = read_input(DAY)

    print(f"===== Ludwig's Advent Of Code 2024 =====\nDay: {DAY}\n\nPart 1:")
    start1 = time.perf_counter()
    res1 = module.part1(task_input)
    time1 = time.perf_counter() - start1
    print(res1)

    print("\nPart 2:")
    start2 = time.perf_counter()
    res2 = module.part2(task_input)
    time2 = time.perf_counter() - start2
    print(res2)

    if time1 >= 0.8:
        print(f"\nPart 1 executed in {time1:.1f} seconds.")
    if time2 >= 0.8:
        print(f"\nPart 2 executed in {time2:.1f} seconds.")

    input()


if __name__ == '__main__':
    main()
