with open('inputs/day_8_test.txt', 'r') as f:
    test_lines = f.readlines()

with open('inputs/day_8.txt', 'r') as f:
    input_lines = f.readlines()


def parse_lines(lines):
    grid = []
    for line in lines:
        grid.append([int(ch) for ch in line.strip()])
    return grid


def viewable_trees(row, col, direction):
    trees_seen = 0
    own_size = grid[row][col]
    blocked = False
    largest_seen = -1
    row += direction[0]
    col += direction[1]
    while (0 <= row < len(grid)) and (0 <= col < len(grid[row])):

        if grid[row][col] > largest_seen:
            largest_seen = grid[row][col]
        if not blocked:
            trees_seen += 1
        else:
            if grid[row][col] > largest_seen:
                trees_seen += 1
        if grid[row][col] >= own_size:
            blocked = True
        row += direction[0]
        col += direction[1]
    return trees_seen


def count_los_from(row, col, direction):
    visible_coords = set()
    largest_tree = -1
    while (0 <= row < len(grid)) and (0 <= col < len(grid[row])):
        if grid[row][col] > largest_tree:
            largest_tree = grid[row][col]
            visible_coords.add(f'{row}-{col}')
        row += direction[0]
        col += direction[1]
    return visible_coords


grid = parse_lines(input_lines)
visible_trees_set = set()
for r in range(len(grid)):
    left_to_right = count_los_from(r, 0, (0, 1))
    right_to_left = count_los_from(r, len(grid[r]) - 1, (0, -1))
    visible_trees_set.update(left_to_right)
    visible_trees_set.update(right_to_left)

for c in range(len(grid[0])):
    top_to_bottom = count_los_from(0, c, (1, 0))
    bottom_to_top = count_los_from(len(grid) - 1, c, (-1, 0))
    visible_trees_set.update(top_to_bottom)
    visible_trees_set.update(bottom_to_top)

print(len(visible_trees_set))

max_score = 0
for r in range(len(grid)):
    for c in range(len(grid[r])):
        left = viewable_trees(r, c, (0, -1))
        right = viewable_trees(r, c, (0, 1))
        up = viewable_trees(r, c, (-1, 0))
        down = viewable_trees(r, c, (1, 0))
        score = left * right * up * down
        if score > max_score:
            max_score = score

print(max_score)
