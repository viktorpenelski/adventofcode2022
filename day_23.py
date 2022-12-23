from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Dict, Set, List, Iterable

from util import timed, result_printing


@dataclass(frozen=True)
class Pos:
    row: int
    col: int

    def adjacent(self) -> Set['Pos']:
        adjacent_positions = set([Pos(self.row + r, self.col + c) for r in [-1, 0, 1] for c in [-1, 0, 1]])
        adjacent_positions.remove(self)
        return adjacent_positions


def parse_inputs(inputs: List[str]) -> Set[Pos]:
    elves = set()
    for r in range(len(inputs)):
        for c in range(len(inputs[r])):
            if inputs[r][c] == '#':
                elves.add(Pos(r, c))
    return elves


DIRECTION_RULES = [
    [Pos(-1, 0), Pos(-1, 1), Pos(-1, -1)],
    [Pos(1, 0), Pos(1, 1), Pos(1, -1)],
    [Pos(0, -1), Pos(-1, -1), Pos(1, -1)],
    [Pos(0, 1), Pos(-1, 1), Pos(1, 1)]
]


def take_turn(elves: Set[Pos], rules: Iterable[List[Pos]]) -> Set[Pos]:
    proposed_moves: Dict[Pos, Pos] = {}
    proposed_counts: Dict[Pos, int] = defaultdict(lambda: 0)
    for elf in elves:
        adjacent = elf.adjacent()
        if adjacent.isdisjoint(elves):
            proposed_moves[elf] = elf
            proposed_counts[elf] = proposed_counts[elf] + 1
        else:
            for rule in rules:
                propositions = [Pos(elf.row + step.row, elf.col + step.col) for step in rule]
                if set(propositions).isdisjoint(elves):
                    move = propositions[0]
                    proposed_moves[elf] = move
                    proposed_counts[move] = proposed_counts[move] + 1
                    break
            if proposed_moves.get(elf) is None:
                proposed_moves[elf] = elf
                proposed_counts[elf] = proposed_counts[elf] + 1
    moves = set()
    for elf, proposed_move in proposed_moves.items():
        if proposed_counts[proposed_move] > 1:
            moves.add(elf)
        else:
            moves.add(proposed_move)

    return moves


def empty_spaces(elves: Set[Pos]) -> int:
    min_row = min([e.row for e in elves])
    min_col = min([e.col for e in elves])
    max_row = max([e.row for e in elves])
    max_col = max([e.col for e in elves])
    row_len = max_row - min_row + 1
    col_len = max_col - min_col + 1
    area = row_len * col_len
    return area - len(elves)


def draw(elves: Set[Pos]) -> str:
    min_row = min([e.row for e in elves])
    min_col = min([e.col for e in elves])
    max_row = max([e.row for e in elves])
    max_col = max([e.col for e in elves])
    state = ""
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if Pos(row, col) in elves:
                state += "#"
            else:
                state += "."
        state += "\n"
    return state


@timed
@result_printing
def solve_pt_1(inputs: List[str]):
    elves: Set[Pos] = parse_inputs(inputs)
    rules = deque(DIRECTION_RULES)
    for _ in range(10):
        elves = take_turn(elves, rules)
        rules.append(rules.popleft())
    print(draw(elves))
    return empty_spaces(elves)


@timed
@result_printing
def solve_pt_2(inputs: List[str]):
    elves: Set[Pos] = parse_inputs(inputs)
    rules = deque(DIRECTION_RULES)
    r = 0
    while True:
        r += 1
        next_elves = take_turn(elves, rules)
        if elves == next_elves:
            break
        elves = next_elves
        rules.append(rules.popleft())
    print(draw(elves))
    return r


if __name__ == '__main__':
    with open('inputs/day_23.txt', 'r') as f:
        lines = f.readlines()
    solve_pt_1(lines)
    solve_pt_2(lines)
