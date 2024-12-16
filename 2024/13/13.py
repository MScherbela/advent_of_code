# %%
import re
import numpy as np


def parse_input(fname):
    data = []
    with open(fname) as f:
        while True:
            lines = [f.readline().strip() for _ in range(4)]
            if len(lines[0]) == 0:
                break
            M = np.zeros([2, 2], int)
            match1 = re.match(r"Button A: X\+(\d*), Y\+(\d*)", lines[0])
            match2 = re.match(r"Button B: X\+(\d*), Y\+(\d*)", lines[1])
            match3 = re.match(r"Prize: X=(\d*), Y=(\d*)", lines[2])
            M[0, 0] = int(match1[1])
            M[0, 1] = int(match2[1])
            M[1, 0] = int(match1[2])
            M[1, 1] = int(match2[2])
            price_pos = np.array([int(match3[1]), int(match3[2])])
            data.append((M, price_pos))
    return data


def get_cost(M, price_pos):
    cost_per_push = np.array([3, 1], int)
    n_pushes = np.linalg.solve(M, price_pos)
    n_pushes_rounded = np.round(n_pushes).astype(int)
    if np.all(M @ n_pushes_rounded == price_pos):
        return np.sum(n_pushes_rounded * cost_per_push)
    return 0


data = parse_input("input.txt")

part1 = 0
part2 = 0
for M, price_pos in data:
    part1 += get_cost(M, price_pos)
    part2 += get_cost(M, price_pos + 10000000000000)

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
