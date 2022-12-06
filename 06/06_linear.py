import queue

with open("06/input.txt") as f:
    stream = f.read()

marker_size = 14
buffer = queue.Queue()
counter = dict()
for i,c in enumerate(stream):
    # Add element
    buffer.put(c)
    if c in counter:
        counter[c] += 1
    else:
        counter[c] = 1

    # Remove elements
    if buffer.qsize() <= marker_size:
        continue
    c = buffer.get()
    counter[c] -= 1
    if counter[c] == 0:
        del counter[c]

    if len(counter) == marker_size:
        print(i+1)
        break




