import parse
import dataclasses
from typing import Tuple
from math import ceil


@dataclasses.dataclass
class Blueprint:
    id: int
    cost_ore: int
    cost_clay: int
    cost_obsidian: Tuple[int, int]
    cost_geode: Tuple[int, int]


class State:
    def __init__(self, t_remain, ore=0, clay=0, obsidian=0, rob_ore=1, rob_clay=0, rob_obsidian=0):
        self.t_remain: int = t_remain
        self.ore: int = ore
        self.clay: int = clay
        self.obsidian: int = obsidian
        self.rob_ore: int = rob_ore
        self.rob_clay: int = rob_clay
        self.rob_obsidian: int = rob_obsidian

    def can_build_ore_robot(self, bp: Blueprint):
        can_afford = (self.ore + self.t_remain * self.rob_ore) >= bp.cost_ore
        useful = self.rob_ore < max(bp.cost_ore, bp.cost_clay, bp.cost_obsidian[0], bp.cost_geode[0])
        return can_afford and useful

    def can_build_clay_robot(self, bp: Blueprint):
        can_afford = (self.ore + self.t_remain * self.rob_ore) >= bp.cost_clay
        useful = self.rob_clay < bp.cost_obsidian[1]
        return can_afford and useful

    def can_build_obsidian_robot(self, bp: Blueprint):
        enough_ore = (self.ore + self.t_remain * self.rob_ore) >= bp.cost_obsidian[0]
        enough_clay = (self.clay + self.t_remain * self.rob_clay) >= bp.cost_obsidian[1]
        useful = self.rob_obsidian < bp.cost_geode[1]
        return enough_ore and enough_clay and useful

    def can_build_geode_robot(self, bp: Blueprint):
        enough_ore = (self.ore + self.t_remain * self.rob_ore) >= bp.cost_geode[0]
        enough_obs = (self.obsidian + self.t_remain * self.rob_obsidian) >= bp.cost_geode[1]
        return enough_ore and enough_obs

    def build_ore_robot(self, bp: Blueprint):
        self.ore -= bp.cost_ore
        self.rob_ore += 1
        return 0

    def build_clay_robot(self, bp: Blueprint):
        self.ore -= bp.cost_clay
        self.rob_clay += 1
        return 0

    def build_obsidian_robot(self, bp: Blueprint):
        self.ore -= bp.cost_obsidian[0]
        self.clay -= bp.cost_obsidian[1]
        self.rob_obsidian += 1
        return 0

    def build_geode_robot(self, bp: Blueprint):
        self.ore -= bp.cost_geode[0]
        self.obsidian -= bp.cost_geode[1]
        return self.t_remain

    @property
    def state(self):
        return (self.t_remain, self.ore, self.clay, self.obsidian, self.rob_ore, self.rob_clay, self.rob_obsidian)

    def advance_time(self, delta_t: int):
        self.t_remain -= delta_t
        self.ore += self.rob_ore * delta_t
        self.clay += self.rob_clay * delta_t
        self.obsidian += self.rob_obsidian * delta_t

    def get_affordable_robots(self, bp):
        return [self.can_build_ore_robot(bp), self.can_build_clay_robot(bp), self.can_build_obsidian_robot(bp), self.can_build_geode_robot(bp)]


    def build_robot(self, robot_type, bp: Blueprint):
        if robot_type == 0:
            delta_t = max(ceil((bp.cost_ore - self.ore) / self.rob_ore), 0) + 1
            self.advance_time(delta_t)
            payoff = self.build_ore_robot(bp)
        if robot_type == 1:
            delta_t = max(ceil((bp.cost_clay - self.ore) / self.rob_ore), 0) + 1
            self.advance_time(delta_t)
            payoff = self.build_clay_robot(bp)
        if robot_type == 2:
            delta_t_1 = max(ceil((bp.cost_obsidian[0] - self.ore) / self.rob_ore), 0) + 1
            delta_t_2 = max(ceil((bp.cost_obsidian[1] - self.clay) / self.rob_clay), 0) + 1
            delta_t = max(delta_t_1, delta_t_2)
            self.advance_time(delta_t)
            payoff = self.build_obsidian_robot(bp)
        if robot_type == 3:
            delta_t_1 = max(ceil((bp.cost_geode[0] - self.ore) / self.rob_ore), 0) + 1
            delta_t_2 = max(ceil((bp.cost_geode[1] - self.obsidian) / self.rob_obsidian), 0) + 1
            delta_t = max(delta_t_1, delta_t_2)
            self.advance_time(delta_t)
            payoff = self.build_geode_robot(bp)
        return payoff


def find_best_move(s: State, cache, bp: Blueprint):
    if s.state in cache:
        return cache[s.state]
    if s.t_remain <= 1:
        return (None, 0)

    best_move = None
    best_payoff = 0
    affordable_robots = s.get_affordable_robots(bp)
    for robot_type, is_affordable in enumerate(affordable_robots):
        if not is_affordable:
            continue
        s_new = State(*s.state)
        payoff = s_new.build_robot(robot_type, bp)
        _, future_payoff = find_best_move(s_new, cache, bp)
        if payoff + future_payoff > best_payoff:
            best_move = robot_type
            best_payoff = payoff + future_payoff

    cache[s.state] = (best_move, best_payoff)
    if len(cache) % 1_000_000 == 0:
        print(f"Cache size: {len(cache)/1e6:.1f} mio")
    return best_move, best_payoff

def get_move_sequence(initial_state, cache, bp: Blueprint):
    s = State(*initial_state.state)
    move_sequence = []
    states = [State(*s.state)]
    while s.state in cache:
        move, _ = cache[s.state]
        if move is None:
            break
        move_sequence.append(move)
        s.build_robot(move, bp)
        states.append(State(*s.state))
    return move_sequence, states

blueprints = []
with open("19/input.txt") as f:
    for line in f:
        match = parse.parse(
            "Blueprint {id:d}: Each ore robot costs {cost_ore:d} ore. Each clay robot costs {cost_clay:d} ore. Each obsidian robot costs {cost_obsidian_ore:d} ore and {cost_obsidian_clay:d} clay. Each geode robot costs {cost_geode_ore:d} ore and {cost_geode_obsidian:d} obsidian.",
            line.strip())
        match = match.named
        bp = Blueprint(id=match['id'],
                       cost_ore=match["cost_ore"],
                       cost_clay=match["cost_clay"],
                       cost_obsidian=(match["cost_obsidian_ore"], match["cost_obsidian_clay"]),
                       cost_geode=(match["cost_geode_ore"], match["cost_geode_obsidian"]))
        blueprints.append(bp)

# # part 1
TOTAL_T_REMAIN = 24
all_payoffs = []
all_moves = []
all_states = []
for i, bp in enumerate(blueprints):
    initial_state = State(t_remain=TOTAL_T_REMAIN)
    cache = {}
    _, n_geodes = find_best_move(initial_state, cache, bp)
    moves, states = get_move_sequence(initial_state, cache, bp)
    all_payoffs.append(n_geodes)
    all_moves.append(moves)
    all_states.append(states)
    print(f"ID {i+1}/{len(blueprints)}: {n_geodes} geodes")

total_quality = 0
for i, payoff in enumerate(all_payoffs):
    total_quality += (i+1) * payoff
print("Part 1: ", total_quality)

# part 2
TOTAL_T_REMAIN = 32 # cache-sizes for bp1: 24: 0.8, 25: 2.0, 26: 4.6
all_payoffs = []
all_moves = []
all_states = []
for i, bp in enumerate(blueprints[:3]):
    initial_state = State(t_remain=TOTAL_T_REMAIN)
    cache = {}
    _, n_geodes = find_best_move(initial_state, cache, bp)
    moves, states = get_move_sequence(initial_state, cache, bp)
    all_payoffs.append(n_geodes)
    all_moves.append(moves)
    all_states.append(states)
    print(f"ID {i+1}/{len(blueprints)}: {n_geodes} geodes")

total_quality = 1
for i, payoff in enumerate(all_payoffs):
    total_quality *= payoff
print("Part 2: ", total_quality)
