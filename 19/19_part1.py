import parse
import dataclasses
from typing import Tuple


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
        return self.ore >= bp.cost_ore

    def can_build_clay_robot(self, bp: Blueprint):
        return self.ore >= bp.cost_clay

    def can_build_obsidian_robot(self, bp: Blueprint):
        return (self.ore >= bp.cost_obsidian[0]) and (self.clay >= bp.cost_obsidian[1])

    def can_build_geode_robot(self, bp: Blueprint):
        return (self.ore >= bp.cost_geode[0]) and (self.obsidian >= bp.cost_geode[1])

    @property
    def state(self):
        return (self.t_remain, self.ore, self.clay, self.obsidian, self.rob_ore, self.rob_clay, self.rob_obsidian)

    # def __hash__(self):
    #     return self.t_remain + self.ore*100 + self.clay*10_000 + self.obsidian * 1_000_000 + self.rob_ore * 100_000_000 + self.rob_clay * 10_000_000_000 + self.rob_obsidian * 1_000_000_000_000

    def advance_time(self):
        self.t_remain -= 1
        self.ore += self.rob_ore
        self.clay += self.rob_clay
        self.obsidian += self.rob_obsidian

    def get_affordable_robots(self, bp):
        return [True, self.can_build_ore_robot(bp), self.can_build_clay_robot(bp), self.can_build_obsidian_robot(bp), self.can_build_geode_robot(bp)]
        
    def build_robot(self, robot_type):
        payoff = 0
        if (robot_type == 1) and self.can_build_ore_robot(bp):
            self.ore -= bp.cost_ore
            self.rob_ore += 1
            self.ore -= 1 # compensate for spurious production
        if (robot_type == 2) and self.can_build_clay_robot(bp):
            self.ore -= bp.cost_clay
            self.rob_clay += 1
            self.clay -= 1 # compensate for spurious production
        if (robot_type == 3) and self.can_build_obsidian_robot(bp):
            self.ore -= bp.cost_obsidian[0]
            self.clay -= bp.cost_obsidian[1]
            self.rob_obsidian += 1
            self.obsidian -= 1 # compensate for spurious production
        if (robot_type == 4) and self.can_build_geode_robot(bp):
            self.ore -= bp.cost_geode[0]
            self.obsidian -= bp.cost_geode[1]
            payoff = self.t_remain - 1
        return payoff


def find_best_move(s: State, cache, bp: Blueprint):
    if s.state in cache:
        return cache[s.state]
    if s.t_remain <= 1:
        return (0, 0)

    best_move = 0
    best_payoff = 0
    affordable_robots = s.get_affordable_robots(bp)
    for robot_type, is_affordable in enumerate(affordable_robots):
        if not is_affordable:
            continue
        s_new = State(*s.state)
        if robot_type > 0:
            payoff = s_new.build_robot(robot_type)
        else:
            payoff = 0
        s_new.advance_time()
        _, future_payoff = find_best_move(s_new, cache, bp)
        if payoff + future_payoff > best_payoff:
            best_move = robot_type
            best_payoff = payoff + future_payoff

    cache[s.state] = (best_move, best_payoff)
    if len(cache) % 100_000 == 0:
        print(f"Cache size: {len(cache)/1e6:.1f} mio")
    return best_move, best_payoff

blueprints = []
with open("19/test_input.txt") as f:
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

bp = blueprints[1]
initial_state = State(t_remain=24)
cache = {}
_, n_geodes = find_best_move(initial_state, cache, bp)
print(n_geodes)

s = State(*initial_state.state)
move_sequence = []
t = 1
while s.state in cache:
    move, _ = cache[s.state]
    move_sequence.append(move)
    s.build_robot(move)
    s.advance_time()
    print(f"t={t}, robot={move}, {s.state}")
    t += 1
print(move_sequence)




        


