import os
import pickle
from abc import abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import List, Dict, Optional, Set, Deque, Tuple

from util import timed, result_printing


@dataclass(frozen=True)
class Point:
    row: int
    col: int


@dataclass(frozen=True)
class Entity:
    identity: str

    @abstractmethod
    def auto_step(self) -> Point:
        pass


@dataclass(frozen=True)
class HurricaneLeft(Entity):
    def __init__(self):
        super().__init__('<')

    def auto_step(self) -> Point:
        return Point(0, -1)


@dataclass(frozen=True)
class HurricaneRight(Entity):
    def __init__(self):
        super().__init__('>')

    def auto_step(self) -> Point:
        return Point(0, 1)


@dataclass(frozen=True)
class HurricaneDown(Entity):
    def __init__(self):
        super().__init__('v')

    def auto_step(self) -> Point:
        return Point(1, 0)


@dataclass(frozen=True)
class HurricaneUp(Entity):
    def __init__(self):
        super().__init__('^')

    def auto_step(self) -> Point:
        return Point(-1, 0)


@dataclass(frozen=True)
class World:
    min_pt: Point
    max_pt: Point
    all_states: List[Dict[Point, Set[Entity]]]

    def get_start_pt(self) -> Point:
        return Point(self.min_pt.row - 1, self.min_pt.col)

    def get_end_pt(self) -> Point:
        return Point(self.max_pt.row + 1, self.max_pt.col)


def entity_factory(raw_entity: str) -> Optional[Entity]:
    if raw_entity == '>':
        return HurricaneRight()
    if raw_entity == '<':
        return HurricaneLeft()
    if raw_entity == 'v':
        return HurricaneDown()
    if raw_entity == '^':
        return HurricaneUp()
    return None


def next_state(current_state: Dict[Point, Set[Entity]],
               min_pt: Point,
               max_pt: Point) -> Dict[Point, Set[Entity]]:
    state: Dict[Point, Set[Entity]] = defaultdict(set)
    for pt, entities in current_state.items():
        for entity in entities:
            step = entity.auto_step()
            e_next = Point(pt.row + step.row, pt.col + step.col)
            if min_pt.row <= e_next.row <= max_pt.row and min_pt.col <= e_next.col <= max_pt.col:
                state[e_next].add(entity)
            else:  # wraparound
                if e_next.row < min_pt.row:
                    state[Point(max_pt.row, e_next.col)].add(entity)
                elif e_next.row > max_pt.row:
                    state[Point(min_pt.row, e_next.col)].add(entity)
                elif e_next.col < min_pt.col:
                    state[Point(e_next.row, max_pt.col)].add(entity)
                elif e_next.col > max_pt.col:
                    state[Point(e_next.row, min_pt.col)].add(entity)
                else:
                    raise Exception('invalid state')
    return state


def get_all_states(inputs: List[str], file_name: str) -> World:
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    else:
        state: Dict[Point, Set[Entity]] = defaultdict(set)

        min_r = None
        max_r = None
        min_c = None
        max_c = None
        for r in range(len(inputs)):
            for c in range(len(inputs[r])):
                entity = entity_factory(inputs[r][c])
                if entity:
                    if min_r is None or r < min_r: min_r = r
                    if min_c is None or c < min_c: min_c = c
                    if max_r is None or r > max_r: max_r = r
                    if max_c is None or c > max_c: max_c = c
                    state[Point(r, c)].add(entity)
        states = [state]
        future_state = state
        min_pt = Point(min_r, min_c)
        max_pt = Point(max_r, max_c)
        while True:
            future_state = next_state(future_state, min_pt, max_pt)
            if future_state == state:
                break
            states.append(future_state)
        world = World(min_pt, max_pt, states)
        with open(file_name, 'wb') as f:
            pickle.dump(world, f)
        return world


def next_moves(pt_from: Point, time: int, world: World) -> List[Point]:
    state = world.all_states[time % len(world.all_states)]
    start_pt = world.get_start_pt()
    end_pt = world.get_end_pt()

    available_moves = []
    if pt_from == start_pt:
        available_moves.append(start_pt)
        available_moves.append(world.min_pt)
    if pt_from == end_pt:
        available_moves.append(end_pt)
        available_moves.append(world.max_pt)
    for r, c in [(0, 1), (1, 0), (-1, 0), (0, -1), (0, 0)]:
        pt = Point(pt_from.row + r, pt_from.col + c)
        if pt not in state:
            if (world.min_pt.row <= pt.row <= world.max_pt.row
                    and world.min_pt.col <= pt.col <= world.max_pt.col):
                available_moves.append(pt)
            if pt == world.min_pt:
                available_moves.append(start_pt)
            if pt == world.max_pt:
                available_moves.append(end_pt)
    return available_moves


def bfs(from_pt: Point, to_pt: Point, time: int, world):
    explored = set()
    q: Deque[Tuple[int, Point]] = deque([(time, from_pt)])
    while q:
        time, pt = q.popleft()
        time += 1
        for next_pt in next_moves(pt, time, world):
            if (time, next_pt) not in explored:
                if next_pt == to_pt:
                    return time + 1
                explored.add((time, next_pt))
                q.append((time, next_pt))


@timed
@result_printing
def solve_pt_1(inputs: List[str], states_file: str):
    world = get_all_states(inputs, states_file)
    return bfs(world.get_start_pt(), world.get_end_pt(), 0, world)


@timed
@result_printing
def solve_pt_2(inputs: List[str], states_file: str):
    world = get_all_states(inputs, states_file)
    first_trip = bfs(world.get_start_pt(), world.get_end_pt(), 0, world)
    trip_back = bfs(world.get_end_pt(), world.get_start_pt(), first_trip, world)
    return bfs(world.get_start_pt(), world.get_end_pt(), trip_back, world)


if __name__ == '__main__':
    inputs, cache = 'inputs/day_24.txt', 'real_states.bin'
    test_inputs, test_cache = 'inputs/test_day_24.txt', 'test_states.bin'
    with open(inputs, 'r') as f:
        lines = f.readlines()
    solve_pt_1(lines, cache)
    solve_pt_2(lines, cache)
