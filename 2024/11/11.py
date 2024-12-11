# %%
from collections import Counter


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


def evolve(numbers: Counter[int], n_steps):
    for _ in range(n_steps):
        new_numbers = Counter()
        for x, mult in numbers.items():
            if x == 0:
                new_numbers[1] += mult
            elif n_digits(x) % 2:
                new_numbers[x * 2024] += mult
            else:
                x1, x2 = split(x)
                new_numbers[x1] += mult
                new_numbers[x2] += mult
        numbers = new_numbers
    return numbers


data = parse_input("input.txt")

numbers1 = evolve(data, 25)
print(f"Part 1: {sum(numbers1.values())}")

numbers2 = evolve(data, 75)
print(f"Part 2: {sum(numbers2.values())}")
