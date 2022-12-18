import parse
import dataclasses
from typing import Tuple, Dict


@dataclasses.dataclass
class Node:
    edges: Tuple[str]
    flow_when_open: int


@dataclasses.dataclass(frozen=True, eq=True)
class Player:
    t_remain: int
    pos: str


@dataclasses.dataclass(frozen=True, eq=True)
class State:
    ind_active: int
    players: Tuple[Player]
    closed_valves: tuple


graph = {}
with open("16/input.txt") as f:
    for line in f:
        line = line.strip()
        line = line.replace("valve ", "valves ").replace("leads", "lead").replace("tunnel ", "tunnels ")
        match = parse.parse("Valve {name} has flow rate={flow_when_open:d}; tunnels lead to valves {edges}", line)
        edges = tuple(match.named['edges'].split(", "))
        graph[match.named['name']] = Node(edges=edges, flow_when_open=match.named['flow_when_open'])


def get_shortest_distances(graph: Dict[str, Node]):
    node_keys = list(graph.keys())
    distance = {}
    for n in node_keys:
        distance[n] = {}
        for m in node_keys:
            if n == m:
                distance[n][m] = 0
            elif m in graph[n].edges:
                distance[n][m] = 1
            else:
                distance[n][m] = 1000
    for k in node_keys:
        for i in node_keys:
            for j in node_keys:
                d_indirect = distance[i][k] + distance[k][j]
                if distance[i][j] > d_indirect:
                    distance[i][j] = d_indirect
    return distance


print("Building distance matrix...")
distance_matrix = get_shortest_distances(graph)


def get_possible_moves(player: Player, valves: tuple):
    next_valve_to_open = []
    for n in valves:
        if distance_matrix[player.pos][n] < player.t_remain:
            next_valve_to_open.append(n)
    return next_valve_to_open


def move_player(p: Player, valves, next_valve: str):
    t_remain = p.t_remain - distance_matrix[p.pos][next_valve] - 1
    pos = next_valve
    closed_valves = tuple(n for n in valves if n != next_valve)
    payoff = graph[next_valve].flow_when_open * t_remain
    return Player(t_remain, pos), closed_valves, payoff


def move(s: State, ind_player, m):
    if m == "stop":
        return State(s.ind_active + 1, s.players, s.closed_valves), 0
    if ind_player == 0:
        p, valves, payoff = move_player(s.players[0], s.closed_valves, m)
        return State(s.ind_active, (p, s.players[1]), valves), payoff
    elif ind_player == 1:
        p, valves, payoff = move_player(s.players[1], s.closed_valves, m)
        return State(s.ind_active, (s.players[0], p), valves), payoff


def search_best_next_move(s: State, cache: dict):
    if s in cache:
        return cache[s]

    best_move = (None, None)
    best_payoff = 0
    p = s.players[s.ind_active]
    possible_moves = get_possible_moves(p, s.closed_valves)
    if s.ind_active == 0:
        possible_moves += ("stop",)
    for m in possible_moves:
        s_new, payoff = move(s, s.ind_active, m)
        _, future_payoff = search_best_next_move(s_new, cache)
        payoff += future_payoff
        if payoff > best_payoff:
            best_move = (s.ind_active, m)
            best_payoff = payoff
    cache[s] = (best_move, best_payoff)
    if (len(cache) % 100_000) == 0:
        print(f"Cache size: {len(cache) / 1e6:.1f} mio")
    return best_move, best_payoff


if __name__ == '__main__':
    T_remaining = 26
    state_cache = {}
    initially_closed_valves = tuple(sorted([n for n in graph if graph[n].flow_when_open > 0]))
    initial_state = State(ind_active=0,
                          players=(Player(t_remain=T_remaining, pos="AA"),
                                   Player(t_remain=T_remaining, pos="AA")),
                          closed_valves=initially_closed_valves)
    first_move, payoff = search_best_next_move(initial_state, state_cache)
    print(f"Cache size: {len(state_cache)}")
    print(f"Payoff: {payoff}")

    s = initial_state
    move_sequence = []
    while s in state_cache:
        next_move = state_cache[s][0]
        if next_move[1] is None:
            break
        move_sequence.append(next_move)
        s = move(s, *next_move)[0]
    print(move_sequence)

    # Cache sizes: 16: 0.4, 18: 1.5, 20: 4.4, 22: 11.1, 24: 24.1, 26: 46.8 mio
