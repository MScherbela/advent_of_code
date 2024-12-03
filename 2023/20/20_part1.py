# %%
from modules import parse_input, push_button, build_graph

module_types, inputs, outputs = parse_input("input.txt", get_dependencies=True)
modules, pulse_queue = build_graph(module_types, inputs, outputs)

n_pulses_low, n_pulses_high = 0, 0
for i in range(1000):
    modules, pulse_queue, n_pulses = push_button(modules, pulse_queue)
    n_pulses_low += n_pulses[0]
    n_pulses_high += n_pulses[1]
print("Part 1:", n_pulses_low * n_pulses_high)
