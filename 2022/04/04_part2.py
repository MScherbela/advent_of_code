data = []
with open("04/input.txt") as f:
    for line in f:
        line = line.strip()
        tokens = line.split(",")
        data.append([[int(x) for x in t.split("-")] for t in tokens])

count = 0
for range1, range2 in data:
    if range1[0] > range2[0]:
        # range1 starts later than range2
        range1, range2 = range2, range1
    if range2[0] <= range1[1]:
        count += 1
print(count)

