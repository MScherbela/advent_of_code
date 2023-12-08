#%%
import math

def parse_input(fname):
    with open(fname) as f:
        instructions = f.readline().strip()
        f.readline() # blank line

        nodes = {}
        for line in f:
            nodes[line[:3]] = (line[7:10], line[12:15])
        return instructions, nodes
    
instructions, node_map = parse_input("input.txt")
instructions = [0 if i == "L" else 1 for i in instructions]
n_instructions = len(instructions)

def get_loop(node):
    states_visited = {(node, 0): 0}

    step_counter = 0
    endpoints = []
    while True:
        ins_index = step_counter % n_instructions
        node = node_map[node][instructions[ins_index]]
        step_counter += 1
        state = (node, ins_index)
        if state in states_visited:
            steps_to_loop = states_visited[state]
            loop_length = step_counter - steps_to_loop
            break
        else:
            states_visited[state] = step_counter
        if node[-1] == "Z":
            endpoints.append(step_counter)
    return loop_length, steps_to_loop, endpoints

def get_finishing_times(node, n_unrolls):
    loop_length, steps_to_loop, endpoints = get_loop(node)
    finishing_times = []
    for n in range(n_unrolls):
        for endpoint in endpoints:
            finishing_times.append(endpoint + n * loop_length)
    return finishing_times

starting_nodes = [n for n in node_map if n[-1] == "A"]
loop_lenghts = []
for n in starting_nodes:
    loop_length, steps_to_loop, endpoints = get_loop(n)
    assert len(endpoints) == 1
    assert endpoints[0] == loop_length
    loop_lenghts.append(loop_length)

print(math.lcm(*loop_lenghts))


