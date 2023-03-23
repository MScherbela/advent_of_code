from typing import List
import numpy as np

class Node:
    def __init__(self, name, operation, dependencies, value):
        self.name = name
        self.operation = operation
        self.dependencies = dependencies
        self.value = value

    @classmethod
    def from_input(cls, line):
        name, instructions = line.strip().split(": ")
        try:
            value = int(instructions)
            operation = None
            dependencies = []
        except ValueError:
            value = None
        if value is None:
            operation = instructions[5]
            assert operation in ["+", "-", "*", "/"]
            dependencies = instructions.split(" " + operation + " ")
        return cls(name, operation, dependencies, value)

    def __repr__(self):
        return f"Node(name={self.name}, operation={self.operation}, dependencies={self.dependencies}, value={self.value})"

    def evaluate(self, *args):
        if self.operation is None:
            return self.value
        elif self.operation == "+":
            return args[0] + args[1]
        elif self.operation == "-":
            return args[0] - args[1]
        elif self.operation == "*":
            return args[0] * args[1]
        elif self.operation == "/":
            return args[0] / args[1]
        else:
            raise ValueError("Undefined operation")

def topological_sort(nodes: List[Node]):
    # Build forward and reverse lookup: which nodes depend on this given node
    nodes = {n.name: n for n in nodes}
    dependency_for = {n: [] for n in nodes}
    depends_on = {n: set() for n in nodes}
    for node_name, node in nodes.items():
        for dep_name in node.dependencies:
            dependency_for[dep_name].append(node_name)
            depends_on[node_name].add(dep_name)

    resolved_nodes = {name for name, node in nodes.items() if len(node.dependencies) == 0}
    sorted_nodes = []
    while resolved_nodes:
        node_name = resolved_nodes.pop()
        sorted_nodes.append(nodes[node_name])
        for next_name in dependency_for[node_name]:
            depends_on[next_name].remove(node_name)
            if len(depends_on[next_name]) == 0:
                resolved_nodes.add(next_name)
    return sorted_nodes


nodes = []
with open("21/input.txt") as f:
    for line in f:
        nodes.append(Node.from_input(line))

def evaluate_graph(nodes_sorted: List[Node]):
    values = {}
    for n in nodes_sorted:
        arguments = [values[dep] for dep in n.dependencies]
        values[n.name] = n.evaluate(*arguments)
    return values

nodes_sorted = topological_sort(nodes)

input_index, input_node = [(i,n) for i,n in enumerate(nodes_sorted) if n.name == "humn"][0]
root_index, root_node = [(i,n) for i,n in enumerate(nodes_sorted) if n.name == "root"][0]
root_node.operation = "-"

def func(x):
    nodes_sorted[input_index].value = x
    return evaluate_graph(nodes_sorted)['root']

bracket = [3e12, 4e12]
bracket_values = [func(x) for x in bracket]

n_iterations = 100
for n in range(n_iterations):
    pivot = np.round((bracket[0] + bracket[1]) / 2)
    pivot_value = func(pivot)
    print(bracket, pivot, pivot_value)
    if abs(pivot_value) < 1:
        break
    if pivot_value * bracket[0] > 0:
        bracket[0] = pivot
    else:
        bracket[1] = pivot

print(int(pivot))
