from dataclasses import dataclass

with open('inputs/day_9_test.txt', 'r') as f:
    test_inputs = [l.strip() for l in f.readlines()]

with open('inputs/day_9.txt', 'r') as f:
    inputs = [l.strip() for l in f.readlines()]


@dataclass
class Coordinates:
    x: int
    y: int

    def touching(self, other: 'Coordinates') -> bool:
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def move(self, direction: str) -> 'Coordinates':
        if 'U' == direction:
            return Coordinates(self.x-1, self.y)
        if 'D' == direction:
            return Coordinates(self.x+1, self.y)
        if 'L' == direction:
            return Coordinates(self.x, self.y-1)
        if 'R' == direction:
            return Coordinates(self.x, self.y+1)
        raise Exception('direction should have been one of U D L R')

    def move_towards(self, other: 'Coordinates') -> 'Coordinates':
        if self.x == other.x:
            if self.y < other.y:
                return self.move('R')
            if self.y > other.y:
                return self.move('L')
            return self
        if self.y == other.y:
            if self.x < other.x:
                return self.move('D')
            if self.x > other.x:
                return self.move('U')
            return self

        # .T...    .....
        # .....    ..T..
        # ...H. -> ...H.
        # .....    .....
        # .....    .....
        if self.x < other.x and self.y < other.y:
            down = self.move('D')
            return down.move('R')

        # ....T    .....
        # .....    ...T.
        # ...H. -> ...H.
        # .....    .....
        # .....    .....
        if self.x < other.x and self.y > other.y:
            down = self.move('D')
            return down.move('L')

        # .....    .....
        # .....    .....
        # ...H. -> ...H.
        # .....    ..T..
        # .T...    .....
        if self.x > other.x and self.y < other.y:
            up = self.move('U')
            return up.move('R')

        # .....    .....
        # .....    .....
        # ...H. -> ...H.
        # .....    ...T.
        # ....T    .....
        if self.x > other.x and self.y > other.y:
            up = self.move('U')
            return up.move('L')

        raise Exception("Should have moved, but didn't. Panik!")

    def __hash__(self):
        return self.x * self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'[{self.x}:{self.y}]'


def solve_for_rope_of_size(size: int) -> int:
    rope = [Coordinates(0, 0)] * size
    visited = set()
    for line in inputs:
        direction, steps = line.split(' ')
        for _ in range(int(steps)):
            rope[0] = rope[0].move(direction)
            for i in range(1, len(rope)):
                if not rope[i].touching(rope[i - 1]):
                    rope[i] = rope[i].move_towards(rope[i - 1])
            visited.add(rope[-1])
    return len(visited)


print(solve_for_rope_of_size(2))
print(solve_for_rope_of_size(10))


