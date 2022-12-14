import ast
import enum
import functools

class Comparison(enum.IntEnum):
    CORRECT = -1
    WRONG = 1
    UNDECIDED = 0


with open("13/input.txt") as f:
    content = f.read()
    samples = content.split("\n\n")
    pairs = []
    for s in samples:
        pairs.append([ast.literal_eval(x) for x in s.split("\n")])

def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return Comparison.CORRECT
        elif a > b:
            return Comparison.WRONG
        else:
            return Comparison.UNDECIDED
    if isinstance(a, int) and isinstance(b, list):
        return compare([a], b)
    if isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])
    if isinstance(a, list) and isinstance(b, list):
        for i in range(min(len(a), len(b))):
            result = compare(a[i], b[i])
            if result != Comparison.UNDECIDED:
                return result
        return compare(len(a), len(b))

# part1
output = 0
for i, p in enumerate(pairs):
    if compare(*p) == Comparison.CORRECT:
        output += (i+1)
print(output)

divider_packets = [[[2]], [[6]]]
all_packets = [*divider_packets]
for p in pairs:
    all_packets += p

all_packets = sorted(all_packets, key=functools.cmp_to_key(compare))
output = 1
for d in divider_packets:
    output = output * (all_packets.index(d)+1)
print(output)



