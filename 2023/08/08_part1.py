#%%
def parse_input(fname):
    with open(fname) as f:
        instructions = f.readline().strip()
        f.readline() # blank line

        nodes = {}
        for line in f:
            nodes[line[:3]] = (line[7:10], line[12:15])
        return instructions, nodes
    
instructions, nodes = parse_input("input.txt")
instructions = [0 if i == "L" else 1 for i in instructions]
n_instructions = len(instructions)

node = "AAA"
step_counter = 0
while node != "ZZZ":
    node = nodes[node][instructions[step_counter % n_instructions]]
    step_counter += 1
    if step_counter % 10_000 == 0:
        print(step_counter)
print(f"Steps (part1): {step_counter}")



