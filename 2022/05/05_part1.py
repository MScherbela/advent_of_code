import re
import queue

initial_stacking = []
moves = []

parse_initial_stacking = True
with open("05/input.txt") as f:
    for line in f:
        line.strip()
        if (len(line) == 0) or "[" not in line:
            parse_initial_stacking = False
        if parse_initial_stacking:
            for i in range(1, len(line), 4):
                if line[i] != " ":
                    initial_stacking.append([i//4, line[i]])
        else:
            m = re.match(R"move (\d*) from (\d*) to (\d*)", line)
            if m:
                moves.append([int(m[1]), int(m[2]) - 1, int(m[3]) - 1])

N_queues = 9
queues = [queue.LifoQueue() for _ in range(N_queues)]
for i, content in reversed(initial_stacking):
    queues[i].put(content)

for n, ind_from, ind_to in moves:
    for _ in range(n):
        queues[ind_to].put(queues[ind_from].get())

final_state = "".join([q.get() for q in queues])
print(final_state)
