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

total_priority = 0
for i1, i2 in data:
    double_set = set(i1).intersection(set(i2))
    assert len(double_set) == 1
    total_priority += list(double_set)[0]
print(total_priority)
