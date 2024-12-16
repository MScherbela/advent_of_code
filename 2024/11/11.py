# %%
from collections import Counter
import time


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


def evolve(numbers: Counter[int], n_steps, mod=None):
    for _ in range(n_steps):
        new_numbers = Counter()
        for x, mult in numbers.items():
            if x == 0:
                new_numbers[1] += mult
            elif n_digits(x) % 2:
                if mod:
                    new_numbers[x * 2024] = (new_numbers[x * 2024] + mult) % mod
                else:
                    new_numbers[x * 2024] += mult
            else:
                x1, x2 = split(x)
                if mod:
                    new_numbers[x1] = (new_numbers[x1] + mult) % mod
                    new_numbers[x2] = (new_numbers[x2] + mult) % mod
                else:
                    new_numbers[x1] += mult
                    new_numbers[x2] += mult

        numbers = new_numbers
    return numbers


data = parse_input("input.txt")

mod = 2024
steps_done = 0
t = time.perf_counter()
for steps in sorted([64, 256, 1024]):
    data = evolve(data, steps - steps_done, mod)
    steps_done = steps

    n_stones = sum(data.values())
    if mod:
        n_stones = n_stones % mod
    print(f"Stones after {steps:3d} steps: {n_stones}")
print(f"t = {time.perf_counter() - t} sec")
