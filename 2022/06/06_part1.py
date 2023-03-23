with open("06/input.txt") as f:
    stream = f.read().strip()

marker_size = 14 # part1: 4, part2: 14
for i in range(marker_size, len(stream)-1):
    substring = stream[i-marker_size:i]
    if len(set(substring)) == marker_size:
        print(i)
        break


