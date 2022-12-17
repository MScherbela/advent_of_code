import parse
import dataclasses

@dataclasses.dataclass
class Node:
    edges: tuple[str]
    flow_when_open: int

@dataclasses.dataclass(frozen=True, eq=True)
class State:
    t: int
    pos1: str
    pos2: str
    open_valves: tuple

graph = {}
with open("16/input.txt") as f:
    for line in f:
        line = line.strip()
        line = line.replace("valve ", "valves ").replace("leads", "lead").replace("tunnel ", "tunnels ")
        match = parse.parse("Valve {name} has flow rate={flow_when_open:d}; tunnels lead to valves {edges}", line)
        edges = tuple(match.named['edges'].split(", "))
        graph[match.named['name']] = Node(edges=edges, flow_when_open=match.named['flow_when_open'])

T_MAX = 26
MAX_VALVES_TO_OPEN = len([n for n in graph.values() if n.flow_when_open > 0])

def move(s: State, move1: str, move2: str):
    t = s.t + 1
    pos1 = s.pos1
    pos2 = s.pos2
    valves = s.open_valves
    additional_flow = 0

    if move1 == "open":
        valves = tuple(sorted(valves + (s.pos1,)))
        additional_flow += (T_MAX - t) * graph[s.pos1].flow_when_open
    else:
        pos1 = move1

    if move2 == "open":
        valves = tuple(sorted(valves + (s.pos2,)))
        additional_flow += (T_MAX - t) * graph[s.pos2].flow_when_open
    else:
        pos2 = move2

    return State(t, pos1, pos2, valves), additional_flow

def get_possible_moves(pos, open_valves):
    possible_moves = graph[pos].edges
    if (graph[pos].flow_when_open > 0) and (pos not in open_valves):
        possible_moves = possible_moves + ("open", )
    return possible_moves

def search_best_next_move(s: State, cache: dict):
    if s in cache:
        return cache[s]
    if s.t == T_MAX:
        return (None,None), 0

    best_move = (None, None)
    best_payoff = 0
    for m1 in get_possible_moves(s.pos1, s.open_valves):
        for m2 in get_possible_moves(s.pos2, s.open_valves):
            if (s.pos1 == s.pos2) and (m1 == 'open') and (m2 == 'open'):
                continue
            s_new, additional_flow = move(s, m1, m2)
            next_move, payoff = search_best_next_move(s_new, cache)
            payoff += additional_flow
            if payoff > best_payoff:
                best_move = m1,m2
                best_payoff = payoff
    cache[s] = (best_move, best_payoff)
    if (len(cache) % 100_000) == 0:
        print(f"Cache size: {len(cache)/1e6:.1f} mio")
    return best_move, best_payoff

if __name__ == '__main__':
    state_cache = {}
    initial_state = State(t=0, pos1="AA", pos2="AA", open_valves=())
    first_move, payoff = search_best_next_move(initial_state, state_cache)
    print(f"Cache size: {len(state_cache)}")
    print(f"Payoff: {payoff}")

    s = initial_state
    move_sequence = []
    while s in state_cache:
        move_sequence.append(state_cache[s][0])
        s = move(s, *move_sequence[-1])[0]
    print(move_sequence)







