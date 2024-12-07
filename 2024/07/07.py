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


def get_nr_of_solutions(target, values, allow_concat=False):
    if len(values) == 1:
        return 1 if target == values[0] else 0
    if values[0] > target:
        return 0

    n_solutions = 0
    val_sum = values[0] + values[1]
    n_solutions += get_nr_of_solutions(target, [val_sum] + values[2:], allow_concat)

    val_prod = values[0] * values[1]
    n_solutions += get_nr_of_solutions(target, [val_prod] + values[2:], allow_concat)

    if allow_concat:
        val_concat = concat(values[0], values[1])
        n_solutions += get_nr_of_solutions(
            target, [val_concat] + values[2:], allow_concat
        )
    return n_solutions


data = parse_input("input.txt")
part1, part2 = 0, 0
for target, values in data:
    if get_nr_of_solutions(target, values) > 0:
        part1 += target
        part2 += target
    else:
        if get_nr_of_solutions(target, values, allow_concat=True) > 0:
            part2 += target
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
