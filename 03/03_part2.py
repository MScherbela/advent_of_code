def to_priority(c):
    x = ord(c) - ord("a")
    if x < 0:
        x += ord("a") - ord("A") + 26
    return x + 1

data = []
with open("03/input.txt") as f:
    for line in f:
        line = line.strip()
        assert len(line) % 2 == 0
        items = [to_priority(c) for c in line]
        data.append([items[:len(items)//2], items[len(items)//2:]])

assert len(data) % 3 == 0

total_priority = 0
for i, (items1, items2) in enumerate(data):
    items = set(items1).union(set(items2))
    if (i%3) == 0:
        intersection = items
    else:
        intersection = intersection.intersection(items)
    if (i % 3) == 2:
        assert len(intersection) == 1
        total_priority += list(intersection)[0]
print(total_priority)
