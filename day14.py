# from PIL import Image, ImageDraw


def parse_input(task_input: str):
    robots = []
    for r in task_input.split('\n'):
        data = [x[2:] for x in r.split(' ')]
        x = int(data[0].split(',')[0])
        y = int(data[0].split(',')[1])
        vx = int(data[1].split(',')[0])
        vy = int(data[1].split(',')[1])
        robots.append((x, y, vx, vy))
    return robots


def part1(task_input: str):
    cols = 101
    rows = 103

    robots = parse_input(task_input)
    robots_end = []

    for startx, starty, vx, vy in robots:
        x, y = startx, starty
        for t in range(100):
            x = (x + vx) % cols
            y = (y + vy) % rows
        robots_end.append((x, y))

    q1 = len([(x, y) for x, y in robots_end if (x < cols // 2) and (y < rows // 2)])
    q2 = len([(x, y) for x, y in robots_end if (x > cols // 2) and (y < rows // 2)])
    q3 = len([(x, y) for x, y in robots_end if (x < cols // 2) and (y > rows // 2)])
    q4 = len([(x, y) for x, y in robots_end if (x > cols // 2) and (y > rows // 2)])
    return q1 * q2 * q3 * q4


def part2(task_input: str):
    print('This takes about 22 seconds... (depending on the solution for your input, lol)')
    # We are searching for a continuous column of 25 robots because that's what makes a tree.
    cols = 101
    rows = 103
    robots = parse_input(task_input)

    t = 0
    while True:
        t += 1
        robots = [(((x+vx) % cols), ((y+vy) % rows), vx, vy) for x, y, vx, vy in robots]

        pic = [list(' ' * cols) for row in range(rows)]
        for x, y, _, _ in robots:
            pic[y][x] = 'X'

        for y in range(rows - 25):
            for x in range(cols):
                if all(pic[y+i][x] == 'X' for i in range(25)):
                    return t

    # This is how I actually solved it (scrolling through windows explorer thumbnails until I spotted a tree):
    # Using pip install pillow==9.5.0

    # t = 0
    # while True:
    #     t += 1
    #     robots = [(((x+vx) % cols), ((y+vy) % rows), vx, vy) for x, y, vx, vy in robots]

    #     pic = [list(' ' * cols) for row in range(rows)]
    #     for x, y, _, _ in robots:
    #         pic[y][x] = 'X'
    #     pic_str = '\n'.join([''.join(row) for row in pic])

    #     im = Image.new('RGBA', (700, 2000), 'black')
    #     draw = ImageDraw.Draw(im)
    #     w, h = draw.textsize(pic_str)

    #     draw.text(((700-w)/2, (2000-h)/2), pic_str, fill="white")
    #     im.save(f'./pics/{str(t).rjust(5, '0')}.png', 'PNG')
