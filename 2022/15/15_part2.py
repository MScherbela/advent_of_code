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


maximum_xy_pos = 4_000_000

# y_hit == 3400528

for y_to_analyze in range(maximum_xy_pos):
    if (y_to_analyze % 1000) == 0:
        print(y_to_analyze)
    # y_to_analyze = 10
    intervals = [get_covered_interval(s, y_to_analyze) for s in sensors]
    intervals = [i for i in intervals if i]
    coverage_changes = [(i[0], 1) for i in intervals] + [(i[1], -1) for i in intervals]
    coverage_changes = sorted(coverage_changes, key=lambda c: (c[0], -c[1]))

    coverage_start_pos = 0
    coverage_end_pos = maximum_xy_pos
    covered_length = 0
    coverage = 0
    for pos, cov_delta in coverage_changes:
        pos = min(pos, coverage_end_pos)
        if (coverage == 0) and cov_delta > 0:
            last_pos = max(pos, coverage_start_pos)
        if (coverage == 1) and (cov_delta < 0):
            covered_length += (pos - last_pos + 1)
        coverage += cov_delta

    # beacons_on_line = set([(s.xb, s.yb) for s in sensors if s.yb == y_to_analyze])
    # n_beacons_on_line = len(beacons_on_line)
    n_uncovered = coverage_end_pos - coverage_start_pos + 1 - covered_length
    if n_uncovered != 0:
        x_uncovered = last_pos - 1
        y_uncovered = y_to_analyze
        frequency = 4000000 * x_uncovered + y_uncovered
        print(f"Uncovered: x={x_uncovered}, y={y_uncovered}, f={frequency}")
        break
    # print(coverage_end_pos - coverage_start_pos + 1 - covered_length)

