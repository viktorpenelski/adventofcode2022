import math
import multiprocessing as mp
import re
from collections import deque
from dataclasses import dataclass
from functools import cache, reduce
from typing import List, Optional

from util import timed


@dataclass(frozen=True)
class Resources:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0

    def has_enough_for(self, other: 'Resources') -> bool:
        return (
                self.ore - other.ore >= 0
                and self.clay - other.clay >= 0
                and self.obsidian - other.obsidian >= 0
        )

    def plus(self, other: 'Resources') -> 'Resources':
        return Resources(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
        )

    def minus(self, other: 'Resources') -> 'Resources':
        return Resources(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
        )

    def multiply(self, times) -> 'Resources':
        return Resources(
            self.ore * times,
            self.clay * times,
            self.obsidian * times
        )

    def equal_to_or_better(self, other: 'Resources') -> bool:
        return (
                self.ore >= other.ore
                and self.clay >= other.clay
                and self.obsidian >= other.obsidian
        )

    def can_accommodate(self, cost: 'Resources') -> bool:
        if cost.ore > 0 and self.ore == 0:
            return False
        if cost.clay > 0 and self.clay == 0:
            return False
        if cost.obsidian > 0 and self.obsidian == 0:
            return False
        return True


@dataclass(frozen=True)
class Blueprint:
    ore_robot: Resources
    clay_robot: Resources
    obsidian_robot: Resources
    geode_robot: Resources

    def get_robot(self, robot: str) -> Resources:
        if robot == 'ore':
            return self.ore_robot
        if robot == 'clay':
            return self.clay_robot
        if robot == 'obsidian':
            return self.obsidian_robot
        if robot == 'geode':
            return self.geode_robot

    @cache
    def max_production_required(self):
        return Resources(
            ore=max(self.ore_robot.ore, self.clay_robot.ore, self.obsidian_robot.ore, self.geode_robot.ore),
            clay=max(self.ore_robot.clay, self.clay_robot.clay, self.obsidian_robot.clay, self.geode_robot.clay),
            obsidian=max(self.ore_robot.obsidian, self.clay_robot.obsidian, self.obsidian_robot.obsidian,
                         self.geode_robot.obsidian),
        )

    def can_build_now(self, robot: str, res: Resources) -> bool:
        if robot == 'ore':
            return res.has_enough_for(self.ore_robot)
        if robot == 'clay':
            return res.has_enough_for(self.clay_robot)
        if robot == 'obsidian':
            return res.has_enough_for(self.obsidian_robot)
        if robot == 'geode':
            return res.has_enough_for(self.geode_robot)
        raise Exception(f'Panik. Unknown robot type {robot}')

    def cost(self, robot: str) -> Resources:
        if robot == 'ore':
            return self.ore_robot
        if robot == 'clay':
            return self.clay_robot
        if robot == 'obsidian':
            return self.obsidian_robot
        if robot == 'geode':
            return self.geode_robot
        raise Exception(f'Panik. Unknown robot type {robot}')

    @staticmethod
    def from_input_line(line: str) -> 'Blueprint':
        regex = (r'Each ore robot costs (\d+) ore\. '
                 r'Each clay robot costs (\d+) ore\. '
                 r'Each obsidian robot costs (\d+) ore and (\d+) clay\. '
                 r'Each geode robot costs (\d+) ore and (\d+) obsidian\.')
        match = re.search(regex, line)
        return Blueprint(
            ore_robot=Resources(ore=int(match.group(1)), clay=0, obsidian=0),
            clay_robot=Resources(ore=int(match.group(2)), clay=0, obsidian=0),
            obsidian_robot=Resources(ore=int(match.group(3)), clay=int(match.group(4)), obsidian=0),
            geode_robot=Resources(ore=int(match.group(5)), clay=0, obsidian=int(match.group(6)))
        )

    def build_robot(self, state: 'State', robot: str) -> Optional['State']:
        robot_cost = self.get_robot(robot)
        max_req = self.max_production_required()
        if robot == 'ore' and max_req.ore <= (state.production.ore + (state.resources.ore // state.time_left)):
            return None
        if robot == 'clay' and max_req.clay <= (state.production.clay + (state.resources.clay // state.time_left)):
            return None
        if state.resources.ore - robot_cost.ore >= 0:
            ore_in_turns = 0
        elif state.production.ore > 0:
            ore_in_turns = math.ceil((robot_cost.ore - state.resources.ore) / state.production.ore)
        else:
            return None
        if state.resources.clay - robot_cost.clay >= 0:
            clay_in_turns = 0
        elif state.production.clay > 0:
            clay_in_turns = math.ceil((robot_cost.clay - state.resources.clay) / state.production.clay)
        else:
            return None
        if state.resources.obsidian - robot_cost.obsidian >= 0:
            obsidian_in_turns = 0
        elif state.production.obsidian > 0:
            obsidian_in_turns = math.ceil((robot_cost.obsidian - state.resources.obsidian) / state.production.obsidian)
        else:
            return None
        turns = 1 + max(ore_in_turns, clay_in_turns, obsidian_in_turns)
        if turns > state.time_left:
            return None
        geodes = state.geodes
        if robot == 'geode':
            geodes += state.time_left - turns
        resources = state.production.multiply(turns).plus(state.resources).minus(robot_cost)
        return State(
            production=state.production.plus(ROBOT_PRODUCTION[robot]),
            resources=resources,
            time_left=state.time_left - turns,
            geodes=geodes
        )

    def build_robots_skipping(self, state: 'State', max_geodes: int) -> List['State']:
        next_states = []
        for robot in ROBOT_PRODUCTION.keys():
            try_build_robot = self.build_robot(state, robot)
            if try_build_robot is not None:
                max_future_geodes = (try_build_robot.time_left * (try_build_robot.time_left - 1)) // 2
                if try_build_robot.geodes + max_future_geodes >= max_geodes:
                    next_states.append(try_build_robot)
        return next_states


ROBOT_PRODUCTION = {
    'ore': Resources(ore=1),
    'clay': Resources(clay=1),
    'obsidian': Resources(obsidian=1),
    'geode': Resources(),
}

with open('inputs/test_day_19.txt', 'r') as f:
    test_inputs = [Blueprint.from_input_line(line) for line in f.readlines()]

with open('inputs/day_19.txt', 'r') as f:
    inputs = [Blueprint.from_input_line(line) for line in f.readlines()]


@dataclass(frozen=True)
class State:
    production: Resources
    resources: Resources
    time_left: int
    geodes: int


def simulate_bfs(bp: Blueprint, time: int):
    starting_state = State(production=ROBOT_PRODUCTION['ore'], resources=Resources(), time_left=time, geodes=0)
    q = deque([starting_state])

    max_geodes = 0
    while len(q) > 0:
        state = q.popleft()
        max_geodes = max(max_geodes, state.geodes)
        if state.time_left <= 0:
            continue
        next_states = bp.build_robots_skipping(state, max_geodes)
        q.extend(next_states)

    print(f'for bp: {bp}, returning {max_geodes}')
    return max_geodes


@timed
def solve_pt_1(blueprints: List[Blueprint]):
    async_results = []
    with mp.Pool(processes=8) as pool:
        for bp in blueprints:
            async_results.append(pool.apply_async(simulate_bfs, [bp, 24]))
        pool.close()
        pool.join()
    print(sum(i * r.get() for i, r in enumerate(async_results, start=1)))


@timed
def solve_pt_2(blueprints: List[Blueprint]):
    async_results = []
    with mp.Pool(processes=3) as pool:
        for bp in blueprints[:3]:
            async_results.append(pool.apply_async(simulate_bfs, [bp, 32]))
        pool.close()
        pool.join()
    results = [r.get() for r in async_results]
    print(reduce(lambda x, y: x * y, results))


if __name__ == '__main__':
    solve_pt_1(inputs)
    solve_pt_2(inputs)
