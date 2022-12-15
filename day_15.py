from dataclasses import dataclass
from typing import List, Tuple

from util import result_printing, timed


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def manhattan_distance_to(self, pt: 'Point'):
        return abs(self.x - pt.x) + abs(self.y - pt.y)


with open('inputs/test_day_15.txt', 'r') as f:
    test_lines = [l.strip() for l in f.readlines()]

with open('inputs/day_15.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]


def parse_input(rows: List[str]):
    def _parse_row(row: str):
        s = row.lstrip('Sensor at ').split(':')[0].split(",")
        sensor = Point(int(s[0].split("=")[1]), int(s[1].split("=")[1]))
        b = row.split(' closest beacon is at ')[1].split(",")
        beacon = Point(int(b[0].split("=")[1]), int(b[1].split("=")[1]))
        return sensor, beacon

    return [_parse_row(r) for r in rows]


@result_printing
@timed
def solve(rows, target_y):
    sensor_beacon_pairs = parse_input(rows)
    beacons = set([sbp[1] for sbp in sensor_beacon_pairs])
    impossible_beacon_locations = set()
    sensor_distance_map = {}
    for sensor, beacon in sensor_beacon_pairs:
        distance = sensor.manhattan_distance_to(beacon)
        sensor_distance_map[sensor] = distance
        closest_pt_y = Point(sensor.x, target_y)
        distance_to_closest_pt_y = sensor.manhattan_distance_to(closest_pt_y)
        if distance_to_closest_pt_y <= distance:
            for x in range(0, 1 + distance - distance_to_closest_pt_y):
                impossible_beacon_locations.add(Point(sensor.x + x, target_y))
                impossible_beacon_locations.add(Point(sensor.x - x, target_y))

    return len(impossible_beacon_locations - beacons)


def blocked_range_from(sensor: Point, beacon: Point, y):
    distance_to_beacon = sensor.manhattan_distance_to(beacon)
    closest_pt_y = Point(sensor.x, y)
    distance_to_closest_pt_y = sensor.manhattan_distance_to(closest_pt_y)
    if distance_to_closest_pt_y <= distance_to_beacon:
        leftover_dist = distance_to_beacon - distance_to_closest_pt_y
        return sensor.x - leftover_dist, sensor.x + leftover_dist
    return None


def converge_ranges(ranges: List[Tuple[int, int]]):
    if len(ranges) <= 1:
        return ranges
    ranges.sort()
    new_ranges = []
    left, right = ranges[0]
    for r in ranges[1:]:
        next_left, next_right = r
        if right + 1 < next_left:
            new_ranges.append((left, right))
            left, right = r
        else:
            right = max(right, next_right)
    new_ranges.append((left, right))
    return new_ranges


@result_printing
@timed
def solve_pt2(rows, min_y=0, max_y=4000000):
    sensor_beacon_pairs = parse_input(rows)
    for y in range(min_y, max_y + 1):
        blocked_ranges = []
        for sensor, beacon in sensor_beacon_pairs:
            if blocked_range := blocked_range_from(sensor, beacon, y):
                blocked_ranges.append(blocked_range)
        converged_ranges = converge_ranges(blocked_ranges)
        if len(converged_ranges) == 2:
            x = max(converged_ranges[0][0], converged_ranges[1][0]) - 1
            return 4_000_000 * x + y


solve(test_lines, 10)
solve(lines, 2000000)

solve_pt2(test_lines, 0, 20)
solve_pt2(lines, 0, 4000000)
