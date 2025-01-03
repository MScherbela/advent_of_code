# %%
from dataclasses import dataclass
import networkx as nx
import numpy as np


@dataclass
class Node:
    name: str
    op: str
    inputs: list[str]
    val: bool | None


def parse_input(fname):
    nodes = {}
    with open(fname) as f:
        for l in f:
            l = l.strip()
            if len(l) == 0:
                continue
            if ":" in l:
                node, val = l.split(": ")
                nodes[node] = Node(node, op="VAL", inputs=[], val=bool(int(val)))
            if "->" in l:
                inputs, output = l.split(" -> ")
                n1, op, n2 = inputs.split(" ")
                nodes[output] = Node(output, op, [n1, n2], None)
    return nodes


def get_outputs(graph, node_name):
    return [n for n in graph if node_name in graph[n].inputs]


graph = parse_input("input.txt")


def eval_with_dfs(graph, node_name):
    node = graph[node_name]
    if node.val is not None:
        return node.val
    input_values = [eval_with_dfs(graph, input_name) for input_name in node.inputs]

    match node.op:
        case "VAL":
            assert len(input_values) == 1
            node.val = input_values[0]
        case "AND":
            assert len(input_values) == 2
            node.val = np.logical_and(input_values[0], input_values[1])
        case "OR":
            assert len(input_values) == 2
            node.val = np.logical_or(input_values[0], input_values[1])
        case "XOR":
            assert len(input_values) == 2
            node.val = np.logical_xor(input_values[0], input_values[1])
    return node.val


final_nodes = sorted([n for n in graph if n.startswith("z")])
part1 = 0
for i, n in enumerate(final_nodes):
    part1 += eval_with_dfs(graph, n) * 2**i
print(f"Part 1: {part1}")


# %%
graph = parse_input("input.txt")


def swap_nodes(graph, n1, n2):
    graph[n2], graph[n1] = graph[n1], graph[n2]


swaps = [("z10", "vcf"), ("z17", "fhg"), ("z39", "tnc"), ("fsq", "dvb")]
for n1, n2 in swaps:
    swap_nodes(graph, n1, n2)


inputs_x = np.array([0, 1, 0, 1, 0, 1, 0, 1], bool)
inputs_y = np.array([0, 0, 1, 1, 0, 0, 1, 1], bool)
inputs_prev = np.array([0, 0, 0, 0, 1, 1, 1, 1], bool)
expected_z = inputs_x ^ inputs_y ^ inputs_prev
expected_carry = (inputs_x & inputs_y) | (inputs_x & inputs_prev) | (inputs_y & inputs_prev)

n_bits_in = 45
n_bits_out = n_bits_in + 1
output_nodes = [f"z{i:02d}" for i in range(n_bits_out)]
input_nodes_x = [f"x{i:02d}" for i in range(n_bits_in)]
input_nodes_y = [f"y{i:02d}" for i in range(n_bits_in)]


def eval_for_test_input(graph, idx_bit):
    for n in graph:
        graph[n].val = None
    for n in input_nodes_x + input_nodes_y:
        graph[n].val = False
    if idx_bit < n_bits_in:
        graph[f"x{idx_bit:02d}"].val = inputs_x
        graph[f"y{idx_bit:02d}"].val = inputs_y
    if idx_bit > 0:
        graph[f"x{idx_bit-1:02d}"].val = inputs_prev
        graph[f"y{idx_bit-1:02d}"].val = inputs_prev
    for n in graph:
        eval_with_dfs(graph, n)
    return graph[f"z{idx_bit:02d}"].val


for i in range(1, n_bits_out - 1):
    z_out = eval_for_test_input(graph, i)
    if np.any(z_out != expected_z):
        print(i)
        print("Actual:   ", z_out)
        print("Expected: ", expected_z)
        for n in graph:
            if np.all(graph[n].val == expected_z):
                print(f"z{i:02d} = ", n)

part2 = sorted([s[0] for s in swaps] + [s[1] for s in swaps])
part2 = ",".join(part2)
print(f"Part 2: {part2}")


eval_for_test_input(graph, 34)
for n in graph:
    if np.all(graph[n].val == expected_carry):
        print("Carry 34", n)
