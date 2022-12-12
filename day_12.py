from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Dict

with open('inputs/test_day_12.txt', 'r') as f:
    test_lines = [list(l.strip()) for l in f.readlines()]

with open('inputs/day_12.txt', 'r') as f:
    lines = [list(l.strip()) for l in f.readlines()]


def find_pos(state, pos):
    for row in range(len(state)):
        for col in range(len(state[row])):
            if state[row][col] == pos:
                return Point(row, col)


def BFS_OF_SHAAAME(state, nr_steps, c_pos, target_pos, visited):
    # morning brain implemented DFS instead of BFS, which can't actually solve for the actual input
    row, col = c_pos
    target_row, target_col = target_pos
    if row == target_row and col == target_col:
        return nr_steps
    if f'{row}:{col}' in visited:
        return None
    current_hight = ord(state[row][col])
    visited.add(f'{row}:{col}')
    print(f'visiting: {c_pos}; visited: {visited}')
    directions = []
    if row > 0 and current_hight - ord(state[row - 1][col]) >= -1:
        up = BFS_OF_SHAAAME(state, nr_steps + 1, (row - 1, col), target_pos, visited.copy())
        if up is not None:
            directions.append(up)
    if row < len(state) - 1 and current_hight - ord(state[row + 1][col]) >= -1:
        down = BFS_OF_SHAAAME(state, nr_steps + 1, (row + 1, col), target_pos, visited.copy())
        if down is not None:
            directions.append(down)
    if col > 0 and current_hight - ord(state[row][col - 1]) >= -1:
        left = BFS_OF_SHAAAME(state, nr_steps + 1, (row, col - 1), target_pos, visited.copy())
        if left is not None:
            directions.append(left)
    if col < len(state[row]) - 1 and current_hight - ord(state[row][col + 1]) >= -1:
        right = BFS_OF_SHAAAME(state, nr_steps + 1, (row, col + 1), target_pos, visited.copy())
        if right is not None:
            directions.append(right)
    min_steps = min(directions) if directions else None
    return min_steps


@dataclass(frozen=True)
class Point:
    row: int
    col: int


def get_traversable_neighbours_asc(state, pos):
    traversable_neighbours = []
    current_hight = ord(state[pos.row][pos.col])
    if pos.row > 0 and current_hight - ord(state[pos.row - 1][pos.col]) >= -1:
        traversable_neighbours.append(Point(pos.row - 1, pos.col))
    if pos.row < len(state) - 1 and current_hight - ord(state[pos.row + 1][pos.col]) >= -1:
        traversable_neighbours.append(Point(pos.row + 1, pos.col))
    if pos.col > 0 and current_hight - ord(state[pos.row][pos.col - 1]) >= -1:
        traversable_neighbours.append(Point(pos.row, pos.col - 1))
    if pos.col < len(state[pos.row]) - 1 and current_hight - ord(state[pos.row][pos.col + 1]) >= -1:
        traversable_neighbours.append(Point(pos.row, pos.col + 1))
    return traversable_neighbours


def get_traversable_neighbours_desc(state, pos):
    traversable_neighbours = []
    current_hight = ord(state[pos.row][pos.col])
    if pos.row > 0 and current_hight - ord(state[pos.row - 1][pos.col]) <= 1:
        traversable_neighbours.append(Point(pos.row - 1, pos.col))
    if pos.row < len(state) - 1 and current_hight - ord(state[pos.row + 1][pos.col]) <= 1:
        traversable_neighbours.append(Point(pos.row + 1, pos.col))
    if pos.col > 0 and current_hight - ord(state[pos.row][pos.col - 1]) <= 1:
        traversable_neighbours.append(Point(pos.row, pos.col - 1))
    if pos.col < len(state[pos.row]) - 1 and current_hight - ord(state[pos.row][pos.col + 1]) <= 1:
        traversable_neighbours.append(Point(pos.row, pos.col + 1))
    return traversable_neighbours


def dijkstra(state, start, target=None):
    universe: Dict[Optional[Point, int]] = defaultdict(lambda: None)
    current_pos = start
    distance = 0
    visited = set()
    universe[current_pos] = 0

    while True:
        neighbours = (
            get_traversable_neighbours_asc(state, current_pos) if target
            else get_traversable_neighbours_desc(state, current_pos)
        )
        for neighbour in neighbours:
            if neighbour in visited:
                continue
            new_distance = distance + 1
            if universe[neighbour] is None or universe[neighbour] > new_distance:
                universe[neighbour] = new_distance
        universe[current_pos] = distance
        visited.add(current_pos)
        if target and current_pos == target:
            return universe[target]
        if target is None and state[current_pos.row][current_pos.col] == 'a':
            return universe[current_pos]

        candidates = [node for node in universe.items() if node[1] and node[0] not in visited]
        current_pos, distance = sorted(candidates, key=lambda x: x[1])[0]
        # print(f'{current_pos} - {distance}')


def solve(state):
    start = find_pos(state, 'S')
    state[start.row][start.col] = 'a'
    end = find_pos(state, 'E')
    state[end.row][end.col] = 'z'
    print(dijkstra(state, start, end))
    print(dijkstra(state, end, None))


solve(test_lines)
