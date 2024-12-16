# %%
from collections import Counter
import numpy as np
from functools import lru_cache


def matrix_power_with_mod(M, n, mod):
    n_binary = f"{n:b}"[::-1]
    A_final = None
    A = M
    for i, c in enumerate(n_binary):
        if c == "1":
            if A_final is None:
                A_final = A
            else:
                A_final = (A_final @ A) % mod
        A = (A @ A) % mod
        if i % 10 == 0:
            print(f"{i} / {len(n_binary)}")
    return A_final


def build_matrix_power(M, mod=None):
    @lru_cache
    def get_transition_matrix(n_steps: int):
        assert n_steps > 0
        if n_steps == 1:
            return M
        elif n_steps == 2:
            A = M @ M
            if mod:
                A = A % mod
            return A

        p = floor_log2(n_steps)
        rest = n_steps - 2**p
        A = get_transition_matrix(2 ** (p - 1))
        print("Computing matrix product for square")
        A = A @ A
        if mod:
            A = A % mod
        if rest:
            print(f"Computing matrix product for rest {rest}")
            A = A @ get_transition_matrix(rest)
        if mod:
            A = A % mod
        return A

    return get_transition_matrix


def parse_input(fname):
    with open(fname) as f:
        data = f.readline().strip()
    data = [int(x) for x in data.split()]
    return Counter(data)


def n_digits(x):
    return len(str(x))


def split(x):
    s = str(x)
    n = len(s) // 2
    return int(s[:n]), int(s[n:])


def step(x):
    if x == 0:
        return (1,)
    if n_digits(x) % 2:
        return (x * 2024,)
    return split(x)


def find_unique_numbers(starting_numbers):
    edges = {}
    while starting_numbers:
        x = starting_numbers.pop()
        children = step(x)
        edges[x] = children
        for c in children:
            if c not in edges:
                starting_numbers.add(c)
    return edges


def build_transition_matrix(graph):
    numbers = sorted(graph.keys())
    idx = {x: i for i, x in enumerate(numbers)}
    N = len(numbers)
    M = np.zeros([N, N], dtype=np.float64)
    for j, x in enumerate(numbers):
        for c in graph[x]:
            M[idx[c], j] += 1
    return M, numbers, idx


def floor_log2(n):
    power = -1
    while n > 0:
        n //= 2
        power += 1
    return power


data = parse_input("input.txt")
# data = [11, 12, 2024]
data = {k: 1 for k in data}
print("Find graph")
graph = find_unique_numbers(set(data.keys()))
print(f"{len(graph)} unique numbers")

print("Build matrix")
M, numbers, idx = build_transition_matrix(graph)


print("Compute matrix power")
n_steps = int(10**75)
mod = 123456
A = matrix_power_with_mod(M, n_steps, mod)
A = A.astype(np.uint64)

input_vec = np.zeros(len(graph), np.uint64)
for x, mult in data.items():
    input_vec[idx[x]] = mult
output_vec = A @ input_vec
n_stones = np.sum(output_vec)
if mod:
    n_stones = n_stones % mod
print(n_stones)
