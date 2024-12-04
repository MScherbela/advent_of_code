# %%
import numpy as np


def parse_input(fname):
    data = []
    chars = {"X": 0, "M": 1, "A": 2, "S": 3}
    with open(fname) as f:
        for line in f:
            line = line.strip()
            data.append([chars[c] for c in line])
    return np.array(data, int)


def shift(x, shift, axis, padding):
    if shift == 0:
        return x
    assert axis in (0, 1)
    assert shift < x.shape[axis]
    x = np.roll(x, shift, axis)
    if (axis == 0) and (shift > 0):
        x[:shift] = padding
    elif (axis == 0) and (shift < 0):
        x[shift:] = padding
    elif (axis == 1) and (shift > 0):
        x[:, :shift] = padding
    elif (axis == 1) and (shift < 0):
        x[:, shift:] = padding
    return x


def shift2D(x, dr, dc, padding=False):
    x = shift(x, shift=dr, axis=0, padding=padding)
    x = shift(x, shift=dc, axis=1, padding=padding)
    return x


data = parse_input("input.txt")
direction = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
n_matches_total = 0
for dr, dc in direction:
    contains_word = np.ones_like(data, bool)
    for n in range(4):
        shifted = shift2D(data == n, dr * n, dc * n)
        contains_word &= shifted
    n_matches_total += contains_word.sum()

print(f"Total matches (Part 1): {n_matches_total}")


is_A = data == 2
is_M = data == 1
is_S = data == 3
contains_word = is_A
contains_word &= (shift2D(is_M, 1, 1) & shift2D(is_S, -1, -1)) | (
    shift2D(is_M, -1, -1) & shift2D(is_S, 1, 1)
)
contains_word &= (shift2D(is_M, 1, -1) & shift2D(is_S, -1, 1)) | (
    shift2D(is_M, -1, 1) & shift2D(is_S, 1, -1)
)

n_matches_part2 = contains_word.sum()
print(f"Total matches (Part 2): {n_matches_part2}")
