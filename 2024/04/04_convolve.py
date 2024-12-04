# %%
import numpy as np
from scipy.signal import convolve2d


def parse_input(fname):
    data = []
    chars = {"X": 1, "M": 2, "A": 3, "S": 4}
    with open(fname) as f:
        for line in f:
            line = line.strip()
            data.append([chars[c] for c in line])
    return np.array(data, int)


def get_matches(data, masks):
    masks_one_hot = [(m[:, :, None] == char_ids).astype(int) for m in masks]
    data_one_hot = (data[:, :, None] == char_ids).astype(int)

    n_matches_total = 0
    for m in masks_one_hot:
        nonzero_elements = m.sum()
        convolution = 0
        for channel in range(4):
            convolution += convolve2d(
                data_one_hot[:, :, channel], m[:, :, channel], mode="valid"
            )
        n_matches_total += (convolution == nonzero_elements).sum()
    return n_matches_total


data = parse_input("input.txt")
char_ids = np.arange(1, 5)

# Part 1: XMAS
masks_part1 = [
    char_ids[:, None],  # vertical
    char_ids[None, :],  # horizontal
    np.diag(char_ids),  # diagonal
]
masks_flipped = []
for m in masks_part1:
    if m.shape[0] > 1:
        masks_flipped.append(m[::-1])
    if m.shape[1] > 1:
        masks_flipped.append(m[:, ::-1])
    if m.shape[0] > 1 and m.shape[1] > 1:
        masks_flipped.append(m[::-1, ::-1])
masks_part1 = masks_part1 + masks_flipped

# Part 2: X-MAS
mask = np.zeros([3, 3], int)
mask[[0, 2], [0, 0]] = 2  # M
mask[1, 1] = 3  # A
mask[[0, 2], [2, 2]] = 4  # S
masks_part2 = [mask, mask.T, mask[:, ::-1], mask.T[::-1]]

n_matches_part1 = get_matches(data, masks_part1)
n_matches_part2 = get_matches(data, masks_part2)
print(f"Total matches (Part 1): {n_matches_part1}")
print(f"Total matches (Part 2): {n_matches_part2}")
