# %%
from modules import parse_input, push_button, build_graph, ConjunctionWithCallback
import networkx as nx
from collections import deque
import numpy as np
import math

module_types, inputs, outputs = parse_input("input.txt", get_dependencies=True)
modules, pulse_queue = build_graph(module_types, inputs, outputs)


# %%
def get_state(modules):
    return tuple([m.get_state() for m in modules.values()])


def get_subgraph(module_types, inputs, outputs, end_node):
    included_modules = set()
    queue = deque([end_node])
    while queue:
        node = queue.popleft()
        if node not in included_modules:
            included_modules.add(node)
            for i in inputs[node]:
                queue.append(i)
    return (
        {n: module_types[n] for n in included_modules},
        {n: inputs[n] for n in included_modules},
        {n: outputs[n] for n in included_modules},
    )


# # Plot graph
# G = nx.DiGraph()
# for module in modules:
#     G.add_node(module, name=module, type=type(modules[module]).__name__)
# for module in modules.values():
#     for output in module.outputs:
#         G.add_edge(module.name, output)
# nx.write_gexf(G, "graph.gexf")

submodule_ends = inputs[inputs["rx"][0]]
cycle_lenghts = []
for end_node in submodule_ends:
    subgraph = get_subgraph(module_types, inputs, outputs, end_node)
    submodules, queue = build_graph(*subgraph)
    submodules[end_node].outputs = []
    submodules["broadcaster"].outputs = [
        o for o in submodules["broadcaster"].outputs if o in submodules
    ]
    state_dict = {get_state(submodules): 0}

    n_pushes = 0
    output_pulses = dict()

    while True:
        output_pulses[n_pushes] = []

        def callback(src, high):
            if not high:
                print(end_node, n_pushes, high)
            output_pulses[n_pushes].append(high)

        submodules[end_node].pulse = callback
        submodules, queue, _ = push_button(submodules, queue)
        state = get_state(submodules)
        n_pushes += 1
        if state in state_dict:
            print(f"End node {end_node}, Cycle: {n_pushes}={state_dict[state]}")
            cycle_lenghts.append(n_pushes - state_dict[state])
            break
        state_dict[state] = n_pushes

print(math.lcm(*cycle_lenghts))
