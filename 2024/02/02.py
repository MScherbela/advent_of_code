# %%
import numpy as np

data = []
with open("input.txt") as f:
    for l in f:
        data.append(list(map(int, l.split())))


def is_safe(row):
    diffs = np.diff(row)
    return (np.all(diffs > 0) or np.all(diffs < 0)) and np.all(np.abs(diffs) <= 3)


n_safe_part1 = 0
n_safe_part2 = 0
for idx, row in enumerate(data):
    if is_safe(row):
        n_safe_part1 += 1
        n_safe_part2 += 1
        continue
    # Terrible brute-force solution
    for i in range(len(row)):
        remaining_row = row[:i] + row[i + 1 :]
        if is_safe(remaining_row):
            n_safe_part2 += 1
            break


print("Part 1: ", n_safe_part1)
print("Part 2: ", n_safe_part2)
