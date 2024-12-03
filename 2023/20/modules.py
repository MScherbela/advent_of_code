from collections import deque, Counter
import networkx as nx


class Module:
    def __init__(self, name, outputs, queue):
        self.name = name
        self.outputs = outputs
        self.queue = queue

    def register_input(self, source):
        pass

    def send(self, high):
        for output in self.outputs:
            self.queue.append((self.name, output, high))

    def get_state(self):
        return None


class Sink(Module):
    def __init__(self, name, queue):
        super().__init__(name, [], queue)

    def pulse(self, source, high):
        pass


class FlipFlop(Module):
    def __init__(self, name, outputs, queue):
        super().__init__(name, outputs, queue)
        self.state = False

    def pulse(self, source, high):
        if high:
            return
        self.state = not self.state
        self.send(self.state)

    def get_state(self):
        return self.state


class Conjuction(Module):
    def __init__(self, name, outputs, queue):
        super().__init__(name, outputs, queue)
        self.state = dict()

    def register_input(self, source):
        self.state[source] = False

    def pulse(self, source, high):
        self.state[source] = high
        output_pulse = not all(self.state.values())
        self.send(output_pulse)
        return output_pulse

    def get_state(self):
        return tuple(self.state.values())


class ConjunctionWithCallback(Conjuction):
    def __init__(self, name, outputs, queue, callback):
        super().__init__(name, outputs, queue)
        self.callback = callback

    def pulse(self, source, high):
        output_pulse = super().pulse(source, high)
        self.callback(
            (
                source,
                high,
                self.get_state(),
                output_pulse,
            )
        )


class Broadcast(Module):
    def __init__(self, name, outputs, queue):
        super().__init__(name, outputs, queue)

    def pulse(self, source, high):
        self.send(high)


def parse_input(fname, get_dependencies=False):
    module_types = dict()
    inputs_per_module = dict()
    outputs_per_module = dict()

    with open(fname) as f:
        for line in f:
            src, targets = line.strip().split(" -> ")
            targets = targets.split(", ")
            name = src.replace("%", "").replace("&", "")

            outputs_per_module[name] = targets
            module_type = (
                "FlipFlop"
                if src.startswith("%")
                else "Conjuction"
                if src.startswith("&")
                else "Broadcast"
            )
            module_types[name] = module_type

            for target in targets:
                if target not in module_types:
                    module_types[target] = "Sink"
                if target not in inputs_per_module:
                    inputs_per_module[target] = []
                inputs_per_module[target].append(name)
            inputs_per_module["broadcaster"] = []
    return module_types, inputs_per_module, outputs_per_module


def build_graph(module_types, inputs_per_module, outputs_per_module):
    modules = dict()
    pulse_queue = deque()
    for name, module_type in module_types.items():
        if module_type == "Sink":
            modules[name] = Sink(name, pulse_queue)
        elif module_type == "FlipFlop":
            modules[name] = FlipFlop(name, outputs_per_module[name], pulse_queue)
        elif module_type == "Conjuction":
            modules[name] = Conjuction(name, outputs_per_module[name], pulse_queue)
            for input_name in inputs_per_module[name]:
                modules[name].register_input(input_name)
        elif module_type == "Broadcast":
            modules[name] = Broadcast(name, outputs_per_module[name], pulse_queue)
    return modules, pulse_queue


def push_button(modules, pulse_queue):
    # Add initial button pulse to the queue
    pulse_queue.append(("button", "broadcaster", False))
    n_pulses_low, n_pulses_high = 0, 0
    while pulse_queue:
        source, target, high = pulse_queue.popleft()
        if high:
            n_pulses_high += 1
        else:
            n_pulses_low += 1
        modules[target].pulse(source, high)
    return modules, pulse_queue, (n_pulses_low, n_pulses_high)
