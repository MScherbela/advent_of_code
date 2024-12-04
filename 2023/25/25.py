# %%
import numpy as np
import networkx as nx


def parse_input(fname):
    with open(fname) as f:
        lines = [l.strip() for l in f]
    edges = {l.split(":")[0]: l.split(":")[1].split() for l in lines}
    nodes = set(edges.keys())
    for t_list in edges.values():
        nodes.update(t_list)
    nodes = list(nodes)

    adj_matrix = np.zeros((len(nodes), len(nodes)), dtype=int)
    for i, n1 in enumerate(nodes):
        for n2 in edges.get(n1, []):
            adj_matrix[i, nodes.index(n2)] = 1
    adj_matrix = adj_matrix + adj_matrix.T
    return adj_matrix


def karger_contraction(adj_matrix):
    adj_matrix = adj_matrix.copy()
    n_nodes = adj_matrix.shape[0]
    n_merged_nodes = np.ones(n_nodes, dtype=int)
    for step in range(n_nodes - 2):
        # n_edges_per_node = np.sum(adj_matrix > 0, axis=1)
        # i = np.random.choice(n_nodes, p=n_edges_per_node / np.sum(n_edges_per_node))
        i = np.random.choice(np.where(n_merged_nodes > 0)[0])
        j = np.random.choice(np.where(adj_matrix[i])[0])
        # Merge j into i (i remains, j is removed)
        n_merged_nodes[i] += n_merged_nodes[j]
        n_merged_nodes[j] = 0
        adj_matrix[i, :] += adj_matrix[j]
        adj_matrix[:, i] += adj_matrix[j]
        adj_matrix[i, i] = 0
        adj_matrix[:, j] = 0
        adj_matrix[j, :] = 0
    return np.max(adj_matrix), n_merged_nodes[np.nonzero(n_merged_nodes)[0]]


adj_matrix = parse_input("input.txt")
n_nodes = len(adj_matrix)

# Spectral method (Fiedler vector)
degree = np.sum(adj_matrix, axis=0)
laplacian = np.diag(degree) - adj_matrix
eigenvalues, eigenvectors = np.linalg.eigh(laplacian)
fiedler_vec = eigenvectors[:, 1]

n_cluster1 = np.sum(fiedler_vec < 0)
n_cluster2 = n_nodes - n_cluster1
print(f"Part 1 (via Fiedler vector): {n_cluster1 * n_cluster2}")

G = nx.Graph(adj_matrix)
nx.set_node_attributes(G, {i: fiedler_vec[i] for i in range(n_nodes)}, "fiedler")
nx.write_gexf(G, "graph.gexf")

# %%
# Karger contraction
n_steps_max = 1000
for i in range(n_steps_max):
    if i % 50 == 0:
        print("Karger step", i)
    cut, n_nodes = karger_contraction(adj_matrix)
    if cut == 3:
        print(f"Part 1 (via Karger's algorithm): {np.prod(n_nodes)}")
        break
else:
    print("Did not find cut of 3 after", n_steps_max, "steps")
