# %%
import re
from functools import lru_cache


def parse_input(fname):
    with open(fname) as f:
        components = f.readline().strip().split(", ")
        _ = f.readline()  # blank
        patterns = []
        for l in f:
            patterns.append(l.strip())
    return components, patterns


components, patterns = parse_input("input.txt")


@lru_cache
def get_nr_of_matches(pattern):
    n_solutions = 0
    for c in components:
        if not pattern.startswith(c):
            continue
        if len(c) == len(pattern):
            n_solutions += 1
            continue
        n_solutions += get_nr_of_matches(pattern[len(c) :])
    return n_solutions


# Part 1
# regex = re.compile(f"^({"|".join(components)})*$")

part1 = 0
part2 = 0
for p in patterns:
    n_solutions = get_nr_of_matches(p)
    part1 += n_solutions > 1
    part2 += n_solutions

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
