# %%
def parse_input(fname):
    data = []
    with open(fname) as f:
        for l in f:
            target, values = l.strip().split(": ")
            data.append((int(target), [int(x) for x in values.split(" ")]))
    return data


def concat(a, b):
    return int(str(a) + str(b))


def matches_target(target, val, rest, operations):
    new_rest = rest[1:]
    for op in operations:
        new_val = op(val, rest[0])
        if new_rest:
            if (new_val <= target) and matches_target(target, new_val, new_rest, operations):
                return True
        elif new_val == target:
            return True
    return False


data = parse_input("input.txt")

operations = [int.__add__, int.__mul__, concat]
part1, part2 = 0, 0
for target, values in data:
    if matches_target(target, values[0], values[1:], operations[:2]):
        part1 += target
        part2 += target
    elif matches_target(target, values[0], values[1:], operations):
        part2 += target
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
