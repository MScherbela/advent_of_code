import parse
import dataclasses

@dataclasses.dataclass
class Sensor:
    x: int
    y: int
    xb: int
    yb: int

    @property
    def radius(self):
        return abs(self.x - self.xb) + abs(self.y-self.yb)


sensors = []
with open("15/input.txt") as f:
    for line in f:
        match = parse.parse("Sensor at x={x:d}, y={y:d}: closest beacon is at x={xb:d}, y={yb:d}", line.strip())
        sensors.append(Sensor(**match.named))

def get_covered_interval(sensor: Sensor, y):
    r = sensor.radius - abs(sensor.y - y)
    if r <= 0:
        return None
    return sensor.x-r, sensor.x+r

y_to_analyze = 2_000_000
intervals = [get_covered_interval(s, y_to_analyze) for s in sensors]
intervals = [i for i in intervals if i]
coverage_changes = [(i[0], 1) for i in intervals] + [(i[1], -1) for i in intervals]
coverage_changes = sorted(coverage_changes, key=lambda c: (c[0], -c[1]))

covered_length = 0
coverage = 0
for c in coverage_changes:
    if (coverage == 0) and c[1] > 0:
        last_pos = c[0]
    if (coverage == 1) and (c[1] < 0):
        covered_length += (c[0] - last_pos + 1)
    coverage += c[1]

beacons_on_line = set([(s.xb, s.yb) for s in sensors if s.yb == y_to_analyze])
n_beacons_on_line = len(beacons_on_line)
print(covered_length - n_beacons_on_line)

