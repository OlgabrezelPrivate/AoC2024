class File:
    def __init__(self, file_id, offset, length):
        self.file_id = file_id
        self.offset = offset
        self.length = length


def parse_input(task_input: str):
    nums = [int(x) for x in task_input]
    files = []
    offset = 0
    file_id = 0

    for i in range(0, len(nums), 2):
        n = nums[i]
        files.append(File(file_id, offset, n))
        if i+1 < len(nums):
            offset += n + nums[i+1]
            file_id += 1

    return files


def checksum(files):
    res = 0
    for f in files:
        for i in range(f.offset, f.offset + f.length):
            res += f.file_id * i
    return res


def part1(task_input: str):
    print("This takes approximately 10 seconds...")
    files = parse_input(task_input)

    while True:
        first_offset = -1
        offset_idx = -1
        for i in range(len(files) - 1):
            f1 = files[i]
            f2 = files[i+1]
            if f1.offset + f1.length < f2.offset:
                first_offset = f1.offset + f1.length
                offset_idx = i+1
                break

        if first_offset == -1:
            break

        last = files[-1]
        last.length -= 1
        if last.file_id == f1.file_id:
            f1.length += 1
        else:
            files.insert(offset_idx, File(last.file_id, first_offset, 1))
        if last.length == 0:
            files.remove(last)

    return checksum(files)


def part2(task_input: str):
    print("This takes approximately 4 seconds...")
    files = parse_input(task_input)

    i = len(files) - 1
    while i >= 0:
        file = files[i]
        for j in range(i):
            if files[j+1].offset - files[j].offset - files[j].length >= file.length:
                del files[i]
                files.insert(j+1, file)
                file.offset = files[j].offset + files[j].length
                break
        else:
            i -= 1

    return checksum(files)
