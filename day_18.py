from collections import defaultdict, deque
from dataclasses import dataclass
from typing import List, Set, Deque
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull
from itertools import chain
import numpy as np

from util import timed, result_printing


@dataclass(frozen=True)
class Point3d:
    x: int
    y: int
    z: int

    def to_list(self) -> List[int]:
        return [self.x, self.y, self.z]

    def is_adjacent(self, pt: 'Point3d') -> bool:
        # two 3d points are adjacent if two of their coordinates are the same
        # and the 3rd has a difference of one
        return 1 == abs(self.x - pt.x) + abs(self.y - pt.y) + abs(self.z - pt.z)

    def sides(self) -> List['Point3d']:
        # a single 1x1x1 cube has 6 "sides" - all adjacent points
        sides = []
        for mod in [-1, 1]:
            sides.append(Point3d(self.x + mod, self.y, self.z))
            sides.append(Point3d(self.x, self.y + mod, self.z))
            sides.append(Point3d(self.x, self.y, self.z + mod))
        return sides

    @staticmethod
    def from_input(line: str) -> 'Point3d':
        x, y, z = [int(num) for num in line.strip().split(',')]
        return Point3d(x, y, z)


def visualize(points: List[List[int]]):
    # plot on a cubic grid with dimensions the one larger than largest coordinate of any point
    dimensions = 1 + max([max(pt) for pt in points])
    # Create axis as our "canvas"
    axes = [dimensions, dimensions, dimensions]

    # Fill in the points
    alpha = 0.7  # transparency of the visualized points

    data = np.zeros(axes, dtype=np.bool_)  # start with all coordinates "False", e.g., w/o 1x1x1 cubes
    colors = np.empty(axes + [4], dtype=np.float32)
    for pt in points:
        data[pt[0]][pt[1]][pt[2]] = True  # fill all x,y,z coordinates that have a point
        colors[pt[0]][pt[1]][pt[2]] = [1, 0, 0, alpha]  # r, g, b

    # Plot figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.voxels(data, facecolors=colors, edgecolors='grey')
    plt.show()


with open('inputs/test_day_18.txt', 'r') as f:
    test_inputs = [Point3d.from_input(line) for line in f.readlines()]

with open('inputs/day_18.txt', 'r') as f:
    inputs = [Point3d.from_input(line) for line in f.readlines()]


@timed
@result_printing
def solve_pt_1(points: Set[Point3d]) -> int:
    mapped_to_sides = map(lambda p: p.sides(), points)  # each point has potentially 6 "open" sides
    all_sides = chain(*mapped_to_sides)  # them to a list of Point3d
    filter_adjacent = filter(lambda p: p not in points, all_sides)  # filter out "blocked" sides
    return len(list(filter_adjacent))  # the remaining sides are going to be the surface area


@timed
@result_printing
def solve_pt_2(points: Set[Point3d]):
    # pretty inefficient to run 6 times over all points, but we know there are not that many of them
    min_pt = Point3d(min(pt.x-1 for pt in points), min(pt.y-1 for pt in points), min(pt.z-1 for pt in points))
    max_pt = Point3d(max([pt.x+1 for pt in points]), max([pt.y+1 for pt in points]), max([pt.z+1 for pt in points]))

    def is_within_bounds(pt: Point3d) -> bool:
        return (
                min_pt.x <= pt.x <= max_pt.x
                and min_pt.y <= pt.y <= max_pt.y
                and min_pt.z <= pt.z <= max_pt.z
        )

    # setup a BFS in 3d space, starting from the top corner
    q: Deque[Point3d] = deque([max_pt])
    visited: Set[Point3d] = set()
    sides = 0
    while len(q) > 0:
        pt = q.popleft()
        if pt not in visited:
            sides_in_bounds = list(filter(lambda p: is_within_bounds(p), pt.sides()))
            next_destinations = list(filter(lambda p: p not in points, sides_in_bounds))
            sides += len(sides_in_bounds) - len(next_destinations)
            q.extend(next_destinations)
            visited.add(pt)
    return sides


solve_pt_1(set(inputs))
solve_pt_2(set(inputs))
visualize([pt.to_list() for pt in inputs])
