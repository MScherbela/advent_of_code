import collections

with open("06/input.txt") as f:
    stream = f.read()

marker_size = 4
buffer = collections.deque()
counter = dict()
for i,c in enumerate(stream):
    # Add element
    buffer.append(c)
    if c in counter:
        counter[c] += 1
    else:
        counter[c] = 1

    # Remove elements
    if len(buffer) <= marker_size:
        continue
    c = buffer.popleft()
    counter[c] -= 1
    if counter[c] == 0:
        del counter[c]

    if len(counter) == marker_size:
        print(i+1)
        break




