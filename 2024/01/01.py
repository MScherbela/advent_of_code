# %%
from collections import Counter

list1 = []
list2 = []
with open("input.txt") as f:
    for l in f:
        a, b = l.split()
        list1.append(int(a))
        list2.append(int(b))

counts_list2 = Counter(list2)

diff_part1 = 0
score_part2 = 0
for x, y in zip(sorted(list1), sorted(list2)):
    diff_part1 += abs(x - y)
    if x in counts_list2:
        score_part2 += x * counts_list2[x]
print("Part 1: ", diff_part1)
print("Part 2: ", score_part2)
