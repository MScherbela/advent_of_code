# %%
from math import gcd


def parse_input(fname):
    data = {}
    with open(fname) as f:
        for i, l in enumerate(f):
            for j, c in enumerate(l.strip()):
                if c != ".":
                    if c not in data:
                        data[c] = []
                    data[c].append((i, j))
    n_rows, n_cols = i + 1, j + 1
    return data, n_rows, n_cols


data, n_rows, n_cols = parse_input("input.txt")

# Part 1
antinodes = set()
for c, positions in data.items():
    for i, (r1, c1) in enumerate(positions):
        for j, (r2, c2) in enumerate(positions):
            if i == j:
                continue
            r = r2 + (r2 - r1)
            c = c2 + (c2 - c1)
            if (0 <= r < n_rows) and (0 <= c < n_cols):
                antinodes.add((r, c))
print(f"Part 1: {len(antinodes)}")

# Part 2
antinodes = set()
for c, positions in data.items():
    for i, (r1, c1) in enumerate(positions):
        for r2, c2 in positions[i + 1 :]:
            dr = r2 - r1
            dc = c2 - c1
            div = gcd(dr, dc)
            dr //= div
            dc //= div

            n_steps_max = max(n_rows, n_cols)
            for sign in [-1, 1]:
                for n in range(n_steps_max):
                    r = r2 + dr * n * sign
                    c = c2 + dc * n * sign
                    if (r < 0) or (r >= n_rows) or (c < 0) or (c >= n_cols):
                        break
                    antinodes.add((r, c))
print(f"Part 2: {len(antinodes)}")
