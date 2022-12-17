import parse
import dataclasses

@dataclasses.dataclass
class Node:
    edges: tuple[str]
    flow_when_open: int

@dataclasses.dataclass(frozen=True, eq=True)
class State:
    t: int
    pos: str
    open_valves: tuple

graph = {}
with open("16/input.txt") as f:
    for line in f:
        line = line.strip()
        line = line.replace("valve ", "valves ").replace("leads", "lead").replace("tunnel ", "tunnels ")
        match = parse.parse("Valve {name} has flow rate={flow_when_open:d}; tunnels lead to valves {edges}", line)
        edges = tuple(match.named['edges'].split(", "))
        graph[match.named['name']] = Node(edges=edges, flow_when_open=match.named['flow_when_open'])

T_MAX = 30
MAX_VALVES_TO_OPEN = len([n for n in graph.values() if n.flow_when_open > 0])

def move(s: State, move: str):
    if move == "open":
        new_state = State(t=s.t+1,
                     pos=s.pos,
                     open_valves=tuple(sorted(s.open_valves + (s.pos,))))
        additional_flow = (T_MAX - s.t - 1) * graph[s.pos].flow_when_open
    else:
        new_state = State(t=s.t+1, pos=move, open_valves=s.open_valves)
        additional_flow = 0
    return new_state, additional_flow

def search_best_next_move(s: State, cache: dict):
    if s in cache:
        return cache[s]
    # for t_ in range(s.t - 1):
    #     if State(t_, s.pos, s.open_valves) in cache:
    #         return None, 0

    possible_moves = graph[s.pos].edges
    if (graph[s.pos].flow_when_open > 0) and (s.pos not in s.open_valves):
        possible_moves = possible_moves + ("open", )

    best_move = None
    best_payoff = -1
    for m in possible_moves:
        s_new, payoff = move(s, m)
        if s_new.t < T_MAX:
            _, future_payoff = search_best_next_move(s_new, cache)
            payoff += future_payoff
        if payoff > best_payoff:
            best_move = m
            best_payoff = payoff
    cache[s] = (best_move, best_payoff)
    if (len(cache) % 100_000) == 0:
        print(f"Cache size: {len(cache)/1e6:.1f} mio")
    return best_move, best_payoff

if __name__ == '__main__':
    state_cache = {}
    initial_state = State(t=0, pos="AA", open_valves=())
    first_move, payoff = search_best_next_move(initial_state, state_cache)
    print(f"Cache size: {len(state_cache)}")
    print(f"Payoff: {payoff}")

    s = initial_state
    move_sequence = []
    while s in state_cache:
        move_sequence.append(state_cache[s][0])
        s = move(s, move_sequence[-1])[0]
    print(move_sequence)







