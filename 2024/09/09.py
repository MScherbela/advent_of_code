# %%
import copy


def insert_node(node, before, after):
    node.prev = before
    node.next = after
    before.next = node
    after.prev = node
    return node


class FileSpace:
    def __init__(self, id, length, prev=None, next=None):
        self.id = id
        self.length = length
        self.prev = prev
        self.next = next
        if prev is not None:
            prev.next = self

    def is_space(self):
        return self.id < 0

    def is_file(self):
        return self.id >= 0

    def __repr__(self):
        prev = f"({self.prev.id}, {self.prev.length})" if self.prev else "(None)"
        next = f"({self.next.id}, {self.next.length})" if self.next else "(None)"
        return f"{prev}, FileSpace({self.id:2d}, {self.length}), {next}"

    def insert_after(self, node):
        return insert_node(node, self, self.next)

    def insert_before(self, node):
        return insert_node(node, self.prev, self)

    def swap_content(self, node):
        self.id, node.id = node.id, self.id
        self.length, node.lenght = node.length, self.length


def parse_input(fname):
    data = []
    is_space = False
    file_id = 0
    with open(fname) as f:
        s = f.read().strip()
    for c in s:
        l = int(c)
        if is_space:
            data.append([-1, l])
        else:
            assert l > 0, "Zero-length file"
            data.append([file_id, l])
            file_id += 1
        is_space = not is_space
    return data


def compact_part1(data):
    data = copy.deepcopy(data)
    idx_space = 1

    while idx_space < len(data):
        file_id, len_file = data[-1]
        len_space = data[idx_space][1]
        if len_file == len_space:
            data[idx_space] = [file_id, len_space]
            idx_space += 2
            data = data[:-2]
        elif len_file > len_space:
            data[idx_space] = [file_id, len_space]
            data[-1][1] -= len_space
            idx_space += 2
        elif len_file < len_space:
            data[idx_space] = [file_id, len_file]
            # Using a doubly linked list would be a better data structure to make this O(1) instead of O(n)
            data = data[: idx_space + 1] + [[-1, len_space - len_file]] + data[idx_space + 1 : -2]
            idx_space += 1
    return data


def checksum(data):
    checksum = 0
    pos = 0
    for file_id, len_file in data:
        for _ in range(len_file):
            checksum += pos * file_id
            pos += 1
    return checksum


def checksum_from_list(node):
    checksum = 0
    pos = 0
    while node is not None:
        for _ in range(node.length):
            if node.is_file():
                checksum += pos * node.id
            pos += 1
        node = node.next
    return checksum


fname = "input.txt"

data = parse_input(fname)
data1 = compact_part1(data)
part1 = checksum(data1)
print(f"Part 1: {part1}")

# Part 2: Convert to linked list
current_file = None
for i, (id, length) in enumerate(data):
    current_file = FileSpace(id, length, current_file)
    if i == 0:
        first = current_file

leftmost_potential_space = {k: first for k in range(1, 10)}
last_id_processed = current_file.id + 1
while last_id_processed > 1:
    # Scan backward until next file to process has been found
    while current_file is not None:
        if current_file.is_file() and (current_file.id < last_id_processed):
            break
        current_file = current_file.prev

        for k, v in leftmost_potential_space.items():
            if current_file == v:
                leftmost_potential_space[k] = None
    last_id_processed = current_file.id

    # Scan forward until a large enough space has been found
    space = leftmost_potential_space[current_file.length]
    while space is not None:
        if space == current_file:
            space = None
            break
        if space.is_space() and (space.length >= current_file.length):
            break
        space = space.next

    leftmost_potential_space[current_file.length] = space

    if space is None:  # no large enough space exists
        continue

    if space.length > current_file.length:
        space = space.insert_before(FileSpace(-1, current_file.length))
        space.next.length -= current_file.length
    space.swap_content(current_file)

part2 = checksum_from_list(first)
print(f"Part 2: {part2}")
