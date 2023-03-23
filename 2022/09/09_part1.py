import numpy as np

data = []
with open("09/input.txt") as f:
    for line in f:
        tokens = line.strip().split(" ")
        data.append([tokens[0], int(tokens[1])])

MOVEMENTS = dict(R=np.array([1,0]),
                 L=np.array([-1,0]),
                 U=np.array([0,1]),
                 D=np.array([0,-1]))

def move(positions, movement):
    new_positions = np.zeros_like(positions)
    for i in range(len(positions)-1):
        new_positions[i], new_positions[i+1] = move_pair(positions[i], positions[i+1], movement)
        movement = new_positions[i+1] - positions[i+1]
    return new_positions

def move_pair(pos_head, pos_tail, movement):
    pos_head = pos_head + movement
    dist = pos_head - pos_tail
    needs_move = np.any(np.abs(dist) > 1)
    if needs_move:
        pos_tail += np.sign(dist)
    return pos_head, pos_tail

len_rope = 10
positions = np.zeros([len_rope, 2], int)

visited_positions = set()
for m, n_steps in data:
    for _ in range(n_steps):
        positions = move(positions, MOVEMENTS[m])
        visited_positions.add(tuple(positions[-1]))
print(len(visited_positions))





