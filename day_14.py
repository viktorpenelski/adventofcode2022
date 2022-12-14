from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, List
import time

from util import timed, result_printing

with open('inputs/test_day_14.txt', 'r') as f:
    test_lines = [l.strip() for l in f.readlines()]

with open('inputs/day_14.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]


@dataclass
class Point:
    x: int
    y: int


class Entity(Enum):
    EMPTY = '  '
    ROCK = '██'
    SAND = '░░'


class IntoTheAbyssException(Exception):
    pass


class World:
    def __init__(self, min_pt: Point, max_pt: Point, abyss: bool):
        if not abyss:
            min_pt = Point(min_pt.x - 400, min_pt.y)
            max_pt = Point(max_pt.x + 400, max_pt.y + 2)
        size_x = max_pt.x - min_pt.x + 1
        size_y = max_pt.y - min_pt.y + 1
        world_map = [[Entity.EMPTY for _ in range(size_x + 1)] for __ in range(size_y)]
        self.map = world_map
        self.min_pt = min_pt
        self.max_pt = max_pt

    def set(self, point: Point, entity: Entity) -> None:
        x_offset = point.x - self.min_pt.x
        y_offset = point.y - self.min_pt.y
        self.map[y_offset][x_offset] = entity

    def get(self, point: Point):
        x_offset = point.x - self.min_pt.x
        y_offset = point.y - self.min_pt.y
        return self.map[y_offset][x_offset]

    def process_sand_abyss(self, sand: Point) -> bool:
        while True:
            try:
                self.get(Point(sand.x, sand.y + 1))
            except:
                raise IntoTheAbyssException()
            if self.get(Point(sand.x, sand.y + 1)) == Entity.EMPTY:
                sand = Point(sand.x, sand.y + 1)
            elif self.get(Point(sand.x - 1, sand.y + 1)) == Entity.EMPTY:
                sand = Point(sand.x - 1, sand.y + 1)
            elif self.get(Point(sand.x + 1, sand.y + 1)) == Entity.EMPTY:
                sand = Point(sand.x + 1, sand.y + 1)
            else:
                if sand == Point(500, 0) and self.get(sand) == Entity.SAND:
                    return False
                self.set(sand, Entity.SAND)
                return True

    def __str__(self):
        rows = ''
        for row in self.map:
            rows += f'{"".join([e.value for e in row])}\n'
        return rows


def parse_input(inputs):
    input_points = []
    min_x = 500
    max_x = 500
    min_y = 0
    max_y = 0
    for line in inputs:
        _line = []
        split = line.split(' -> ')
        for coords in split:
            x, y = coords.split(',')
            point = Point(int(x), int(y))
            _line.append(point)
            if point.x < min_x:
                min_x = point.x
            if point.x > max_x:
                max_x = point.x
            if point.y < min_y:
                min_y = point.y
            if point.y > max_y:
                max_y = point.y
        input_points.append(_line)
    return input_points, (Point(min_x, min_y), Point(max_x, max_y))


def draw_map(all_points: List[List[Point]],
             min_pt: Point,
             max_pt: Point,
             abyss: bool = True):
    world = World(min_pt, max_pt, abyss)
    for points in all_points:
        for i in range(1, len(points)):
            first = points[i - 1]
            second = points[i]
            min_x = min(first.x, second.x)
            max_x = max(first.x, second.x)
            min_y = min(first.y, second.y)
            max_y = max(first.y, second.y)
            if max_x - min_x > 0:
                assert min_y == max_y
                for x in range(min_x, max_x + 1):
                    world.set(Point(x, min_y), Entity.ROCK)
            else:
                for y in range(min_y, max_y + 1):
                    world.set(Point(min_x, y), Entity.ROCK)
    if not abyss:
        for x in range(world.min_pt.x, world.max_pt.x + 1):
            world.set(Point(x, max_pt.y + 2), Entity.ROCK)

    return world


@timed
@result_printing
def solve(inputs):
    rock_coords, (min_pt, max_pt) = parse_input(inputs)
    world = draw_map(rock_coords, min_pt, max_pt)
    total_sand = 0
    sand = Point(500, 0)
    while True:
        # print(world)

        try:
            world.process_sand_abyss(sand)
        except IntoTheAbyssException:
            break
        total_sand += 1
    return total_sand
    # print(world)
    # print(total_sand)


@timed
@result_printing
def solve_pt2(inputs):
    rock_coords, (min_pt, max_pt) = parse_input(inputs)
    world = draw_map(rock_coords, min_pt, max_pt, False)
    total_sand = 0
    sand = Point(500, 0)
    while world.process_sand_abyss(sand):
        total_sand += 1
    # print(world)
    #print(total_sand)
    return total_sand


solve(lines)
solve_pt2(lines)
