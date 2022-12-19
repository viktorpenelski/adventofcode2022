import re
from collections import deque, defaultdict
from dataclasses import dataclass
from functools import cache
from itertools import chain
from typing import List, Set, Deque

from util import timed, result_printing


@dataclass(frozen=True)
class Resources:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geodes: int = 0

    def has_enough_for(self, other: 'Resources') -> bool:
        return (self.ore - other.ore >= 0
                and self.clay - other.clay >= 0
                and self.obsidian - other.obsidian >= 0
                and self.geodes - other.geodes >= 0)

    def plus(self, other: 'Resources') -> 'Resources':
        return Resources(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geodes + other.geodes
        )

    def minus(self, other: 'Resources') -> 'Resources':
        return Resources(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geodes - other.geodes
        )

    def better_than(self, other: 'Resources') -> bool:
        return (
                self.ore >= other.ore
                and self.clay >= other.clay
                and self.obsidian >= other.obsidian
                and self.geodes >= other.geodes
        )


@dataclass(frozen=True)
class Blueprint:
    ore_robot: Resources
    clay_robot: Resources
    obsidian_robot: Resources
    geode_robot: Resources

    @cache
    def max_production_required(self):
        return Resources(
            ore=max(self.ore_robot.ore, self.clay_robot.ore, self.obsidian_robot.ore, self.geode_robot.ore),
            clay=max(self.ore_robot.clay, self.clay_robot.clay, self.obsidian_robot.clay, self.geode_robot.clay),
            obsidian=max(self.ore_robot.obsidian, self.obsidian_robot.obsidian, self.obsidian_robot.obsidian,
                         self.geode_robot.obsidian),
            geodes=max(self.ore_robot.geodes, self.obsidian_robot.geodes, self.obsidian_robot.geodes,
                       self.geode_robot.geodes),
        )

    def can_build(self, robot: str, res: Resources) -> bool:
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

    def robots_to_build(self, state: 'State') -> List[str]:
        if self.can_build('geode', state.resources):
            return ['geode']
        to_build = []
        if (
                self.can_build('ore', state.resources)
                and self.max_production_required().ore - state.production.ore > 0
                and (self.max_production_required().ore - state.production.ore) * state.time_left > state.resources.ore
        ):
            to_build.append('ore')
        if (
                self.can_build('clay', state.resources)
                and self.max_production_required().clay - state.production.clay > 0
                and (
                self.max_production_required().clay - state.production.clay) * state.time_left > state.resources.clay
        ):
            to_build.append('clay')
        if (
                self.can_build('obsidian', state.resources)
                and self.max_production_required().obsidian - state.production.obsidian > 0
                and (
                self.max_production_required().obsidian - state.production.obsidian) * state.time_left > state.resources.obsidian
        ):
            to_build.append('obsidian')
        return to_build


ROBOT_PRODUCTION = {
    'ore': Resources(ore=1),
    'clay': Resources(clay=1),
    'obsidian': Resources(obsidian=1),
    'geode': Resources(geodes=1)
}

with open('inputs/test_day_19.txt', 'r') as f:
    test_inputs = [Blueprint.from_input_line(line) for line in f.readlines()]

with open('inputs/day_19.txt', 'r') as f:
    inputs = [Blueprint.from_input_line(line) for line in f.readlines()]


#
# def simulate_dfs(production: Resources, res: Resources, bp: Blueprint, time_left: int, all_productions) -> Resources:
#     all_productions[time_left].append(production)
#     if time_left <= 0:
#         return res
#     # produce
#     # resources = res.plus(production)
#     # print(f'time_left: {time_left}, collecting: {production}, bank: {res}')
#     if bp.can_build('geode', res):
#         return simulate_dfs(
#             production.plus(ROBOT_PRODUCTION['geode']),
#             res.plus(production).minus(bp.cost('geode')),
#             bp, time_left - 1, all_productions)
#     robots = ['ore', 'clay', 'obsidian']
#     robots = list(filter(lambda r: bp.can_build(r, res), robots))
#     robots = list(filter(lambda r: bp.robots_to_build(r, production, time_left), robots))
#     if len(robots) > 0:
#         simulations = []
#         for robot in robots:
#             # print(f'Beep Boop, creating a [{robot}]. Current production is {production}')
#             result = simulate_dfs(
#                 production.plus(ROBOT_PRODUCTION[robot]),
#                 res.plus(production).minus(bp.cost(robot)),
#                 bp,
#                 time_left - 1,
#                 all_productions
#             )
#             simulations.append(result)
#         simulations.append(simulate_dfs(production, res.plus(production), bp, time_left - 1, all_productions))
#         simulations.sort(key=lambda r: r.geodes, reverse=True)
#         return simulations[0]
#     else:
#         return simulate_dfs(production, res.plus(production), bp, time_left - 1, all_productions)
#

@dataclass(frozen=True)
class State:
    production: Resources
    resources: Resources
    time_left: int


def filter_only_better_states(best_states, states, visited):
    to_return = []
    for state in states:
        if state in visited:
            continue
        if best_states.get(state.time_left) is None:
            to_return.append(state)
        elif (state.resources.better_than(best_states[state.time_left].resources)
              and state.production.better_than(best_states[state.time_left].production)):
            to_return.append(state)
    return states


def simulate_bfs(bp: Blueprint, time: int):
    starting_state = State(production=ROBOT_PRODUCTION['ore'], resources=Resources(), time_left=time)
    q = deque([starting_state])
    best_states = {
        time: starting_state
    }
    visited = set()
    max_geodes = 0
    while len(q) > 0:
        state = q.popleft()
        if state in visited:
            continue
        visited.add(state)
        max_geodes = max(max_geodes, state.resources.geodes)
        if state.time_left <= 0:
            continue
        if state.resources.geodes < max_geodes - 2:
            continue
        if best_states.get(state.time_left) is None:
            best_states[state.time_left] = state
        elif (state.resources.better_than(best_states[state.time_left].resources)
              and state.production.better_than(best_states[state.time_left].production)
        ):
            best_states[state.time_left] = state
        robots = bp.robots_to_build(state)
        next_states = []
        for robot in robots:
            next_states.append(State(
                state.production.plus(ROBOT_PRODUCTION[robot]),
                state.resources.minus(bp.cost(robot)).plus(state.production),
                state.time_left - 1
            ))

        q.extend(filter_only_better_states(best_states, next_states, visited))
        if state.time_left > 7 or len(next_states) == 0:
            q.append(State(state.production, state.resources.plus(state.production), state.time_left - 1))
    return max_geodes


@timed
def solve_pt_1(blueprints: List[Blueprint]):
    results = []
    for i, bp in enumerate(blueprints, start=1):
        results.append(i * simulate_bfs(bp, 24))
    print(sum(results))


solve_pt_1(test_inputs)
