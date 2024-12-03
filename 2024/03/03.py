# %%
import re

with open("input.txt") as f:
    data = f.read().strip()

result_part1 = 0
result_part2 = 0
enabled = True
for match in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", data):
    if match == "do()":
        enabled = True
        continue
    if match == "don't()":
        enabled = False
        continue
    else:
        match = match.replace("mul(", "").replace(")", "")
        x, y = map(int, match.split(","))
        result_part1 += x * y
        if enabled:
            result_part2 += x * y

print(f"Part 1: {result_part1}")
print(f"Part 2: {result_part2}")
