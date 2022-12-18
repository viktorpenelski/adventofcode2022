from dataclasses import dataclass
from enum import Enum
from time import sleep
from typing import List, Tuple

from util import result_printing, timed


class Current(Enum):
    LEFT = '<'
    RIGHT = '>'

    def __str__(self):
        return f'{self.value}'

    @staticmethod
    def from_char(ch: str) -> 'Current':
        if ch == '<':
            return Current.LEFT
        if ch == '>':
            return Current.RIGHT
        raise Exception(f'Unknown token {ch}')


class Entities(Enum):
    EMPTY = ' '
    ROCK_REST = '#'
    ROCK_FALLING = '@'


DASH_ROCK = [
    [Entities.ROCK_FALLING] * 4
]
PLUS_ROCK = [
    [Entities.EMPTY, Entities.ROCK_FALLING, Entities.EMPTY],
    [Entities.ROCK_FALLING] * 3,
    [Entities.EMPTY, Entities.ROCK_FALLING, Entities.EMPTY]
]
REVERSE_L_ROCK = [
    [Entities.EMPTY, Entities.EMPTY, Entities.ROCK_FALLING],
    [Entities.EMPTY, Entities.EMPTY, Entities.ROCK_FALLING],
    [Entities.ROCK_FALLING] * 3
]
VERTICAL_ROCK = [
    [Entities.ROCK_FALLING],
    [Entities.ROCK_FALLING],
    [Entities.ROCK_FALLING],
    [Entities.ROCK_FALLING]
]

SQUARE_ROCK = [
    [Entities.ROCK_FALLING] * 2,
    [Entities.ROCK_FALLING] * 2
]

with open('inputs/test_day_17.txt', 'r') as f:
    test_inputs = [Current.from_char(ch) for ch in f.readline()]

with open('inputs/day_17.txt', 'r') as f:
    inputs = [Current.from_char(ch) for ch in f.readline()]


class NarrowChamber:
    def __init__(self, currents: List[Current]):
        self.currents = currents
        self.rocks = [DASH_ROCK, PLUS_ROCK, REVERSE_L_ROCK, VERTICAL_ROCK, SQUARE_ROCK]
        self.next_rock = 0
        self.next_current = 0
        self.active_rock_start = 0
        self.active_rock_end = 0
        self.world: List[List[Entities]] = [
            [Entities.ROCK_REST] * 7
        ]
        self.compacted_rows = 0
        self.height_history: List[int] = [0]
        self.height_diffs: List[int] = []

    def _add_row(self):
        self.world.append([Entities.EMPTY] * 7)

    def find_top(self) -> int:
        peak = 0
        for i in range(len(self.world)):
            if Entities.ROCK_REST in self.world[i]:
                peak = i
        return peak

    def compact_if_possible(self):
        if len(self.world) < 10:
            return
        top_row = self.find_top()
        for r in range(top_row, top_row - 7, -1):
            wall = True
            for c in range(len(self.world[top_row])):
                if self.world[r][c] == Entities.EMPTY and self.world[r-1][c] == Entities.EMPTY:
                    wall = False
            if wall:
                self.compacted_rows += r - 1
                self.world = self.world[r - 1:]
                return

    def _ensure_3_rows_on_top(self):
        diff = len(self.world) - 1 - self.find_top()
        if diff <= 3:
            for _ in range(min(3, 3 - (len(self.world) - 1 - self.find_top()))):
                self._add_row()
        else:
            for _ in range(diff - 3):
                del self.world[-1]

    def spawn_rock(self):
        #       self.compact_if_possible()
        self._ensure_3_rows_on_top()
        rock = self.rocks[self.next_rock % len(self.rocks)]
        self.active_rock_start = len(self.world)
        for r in range(len(rock) - 1, - 1, -1):
            pad_left = [Entities.EMPTY] * 2
            pad_right = [Entities.EMPTY] * (7 - len(pad_left) - len(rock[r]))
            self.world.append(pad_left + rock[r] + pad_right)
        self.active_rock_end = len(self.world) - 1

        self.next_rock += 1

    def move_rock(self):
        def _jet():
            jet = self.currents[self.next_current % len(self.currents)]
            self.next_current += 1
            if jet == Current.LEFT:
                leftmost_edge = 9
                adjacent = False
                for r in range(self.active_rock_start, self.active_rock_end + 1):
                    for c in range(len(self.world[r])):
                        if self.world[r][c] is Entities.ROCK_FALLING:
                            if c < leftmost_edge:
                                leftmost_edge = c
                            if c > 0 and self.world[r][c - 1] is Entities.ROCK_REST:
                                adjacent = True
                                break
                if leftmost_edge > 0 and not adjacent:
                    for r in range(self.active_rock_start, self.active_rock_end + 1):
                        for c in range(len(self.world[r]) - 1):
                            if self.world[r][c + 1] == Entities.ROCK_FALLING:
                                self.world[r][c] = self.world[r][c + 1]
                                self.world[r][c + 1] = Entities.EMPTY
                        if self.world[r][len(self.world[r]) - 1] == Entities.ROCK_FALLING:
                            self.world[r][len(self.world[r]) - 1] = Entities.EMPTY

            if jet == Current.RIGHT:
                rightmost_edge = 0
                adjacent = False
                for r in range(self.active_rock_start, self.active_rock_end + 1):
                    for c in range(len(self.world[r])):
                        if self.world[r][c] is Entities.ROCK_FALLING:
                            if c > rightmost_edge:
                                rightmost_edge = c
                            if c < len(self.world[r]) - 1 and self.world[r][c + 1] is Entities.ROCK_REST:
                                adjacent = True
                                break
                if rightmost_edge < len(self.world[0]) - 1 and not adjacent:
                    for r in range(self.active_rock_start, self.active_rock_end + 1):
                        for c in range(len(self.world[r]) - 1, 0, -1):
                            if self.world[r][c - 1] == Entities.ROCK_FALLING:
                                self.world[r][c] = self.world[r][c - 1]
                                self.world[r][c - 1] = Entities.EMPTY
                        if self.world[r][0] == Entities.ROCK_FALLING:
                            self.world[r][0] = Entities.EMPTY

        def _down():
            next_row = self.active_rock_start - 1
            for row in range(next_row, self.active_rock_end):
                for col in range(len(self.world[next_row])):
                    if (
                            self.world[row][col] == Entities.ROCK_REST
                            and self.world[row+1][col] == Entities.ROCK_FALLING
                    ):
                        for r in range(self.active_rock_start, self.active_rock_end + 1):
                            for c in range(len(self.world[r])):
                                if self.world[r][c] == Entities.ROCK_FALLING:
                                    self.world[r][c] = Entities.ROCK_REST
                        self.height_diffs.append(self.find_top() - self.height_history[-1])
                        self.height_history.append(self.find_top())
                        return True
            for r in range(next_row, self.active_rock_end):
                for c in range(len(self.world[r])):
                    if self.world[r][c] != Entities.ROCK_REST and self.world[r+1][c] != Entities.ROCK_REST:
                        self.world[r][c] = self.world[r + 1][c]
            self.world[self.active_rock_end] = [Entities.EMPTY if r == Entities.ROCK_FALLING
                                                else r for r in self.world[self.active_rock_end]]
            self.active_rock_start -= 1
            self.active_rock_end -= 1

        _jet()
        return _down()

    def __str__(self):
        world = ''
        for i in range(len(self.world) - 1, -1, -1):
            world += f'{[e.value for e in self.world[i]]}\n'
        return world


@timed
def solve(currents: List[Current], calc_for: int):
    world = NarrowChamber(currents)
    for _ in range(2022):
        world.spawn_rock()
        settle = False
        while not settle:
            settle = world.move_rock()
    print(f'Pt1, height to 2022: {world.find_top()}')
    window = 50
    convince_the_elephants = calc_for
    for start_i in range(len(world.height_diffs) - window):
        matches = []
        diffs = world.height_diffs[start_i:start_i+window]
        for ind in (i for i,e in enumerate(world.height_diffs) if e == diffs[0]):
            if world.height_diffs[ind:ind+window] == diffs:
                matches.append(ind)
        if len(matches) > 1:
            loop_start = matches[0]
            loop_size = matches[1] - matches[0]
            single_loop_height = sum(world.height_diffs[matches[0]:matches[1]])
            height_before_loop = sum(world.height_diffs[:loop_start])
            loops_in_sample = (convince_the_elephants - loop_start) // loop_size
            leftover_after_loops = (convince_the_elephants - loop_start) % loop_size
            leftover_height = sum(world.height_diffs[loop_start:loop_start + leftover_after_loops])
            final_height = height_before_loop + loops_in_sample * single_loop_height + leftover_height
            print(f'Pt2, height to {convince_the_elephants}: {final_height}')
            break


solve(test_inputs, 1_000_000_000_000)
solve(inputs, 1_000_000_000_000)
