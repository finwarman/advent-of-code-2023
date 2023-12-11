#! /usr/bin/env python3
import numpy as np
from collections import deque

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

GRID = np.array([list(row.strip()) for row in data.split('\n')[:-1]])

# ==== SOLUTION ====

# valid chars in each direction
valid_direction_chars = {
    'up':    ('|', '7', 'F'),
    'down':  ('|', 'L', 'J'),
    'left':  ('-', 'L', 'F'),
    'right': ('-', '7', 'J'),
}

# map current char to possible directions
valid_steps = {
    '.': (),
    '|': ('up',   'down'  ),
    '-': ('left', 'right' ),
    'L': ('up',   'right' ),
    'J': ('up',   'left'  ),
    '7': ('down', 'left'  ),
    'F': ('down', 'right' ),
}

# map direction name to (dx, dy) offset
offsets = {
    'up':    ( 0, -1),
    'down':  ( 0,  1),
    'left':  (-1,  0),
    'right': ( 1,  0),
}

# add tuples e.g. (x, y) + (dx, dy)
def add(tuple_a, tuple_b):
    return (tuple_a[0]+tuple_b[0], tuple_a[1]+tuple_b[1])

# get (x, y) positions for each direction name
def get_neighbours(position):
    return {
        'up':    add(position, offsets['up']),
        'down':  add(position, offsets['down']),
        'left':  add(position, offsets['left']),
        'right': add(position, offsets['right']),
    }

# determine only valid char for current position
def get_starting_char(start_pos):
    neighbour_chars = {dir: GRID[y][x] for dir, (x, y) in get_neighbours(start_pos).items()}
    for potential, dirs in valid_steps.items():
        valid = [char for dir, char in neighbour_chars.items() if dir in dirs and char in valid_direction_chars[dir]]
        if len(valid) == 2:
            return potential
    return None

# for current position, get valid steps from that position
# [('down', (1, 2, '|')), ('right', (2, 1, '-'))]
def get_possible_steps(position):
    x, y = position
    char = GRID[y][x]
    neighbours = get_neighbours(position)
    possible_steps = []

    for direction in valid_steps[char]:
        neighbour_x, neighbour_y = neighbours[direction]
        if (0 <= neighbour_x < GRID.shape[1]) and (0 <= neighbour_y < GRID.shape[0]):
            neighbour_char = GRID[neighbour_y][neighbour_x]
            if neighbour_char in valid_direction_chars[direction]:
                possible_steps.append((direction, (neighbour_x, neighbour_y), GRID[neighbour_y][neighbour_x]))

    return possible_steps

# find and set-up start position
s_index = np.where(GRID == 'S')
START_POS  = (s_index[1][0], s_index[0][0])

GRID[START_POS[1]][START_POS[0]] = get_starting_char(START_POS)


# navigate from starting point around the loop
queue, visited = deque([(START_POS, 0)]), {} # (x, y): dist
while queue:
    (x, y), dist = queue.pop()
    visited[(x, y)] = dist

    possible_steps = get_possible_steps((x, y))
    if (x, y) == START_POS: # start in only 1 direction
        possible_steps = [possible_steps[1]]

    for _, (new_x, new_y), _ in possible_steps:
        if (new_x, new_y) not in visited:
            queue.append(((new_x, new_y), dist + 1))

# get loop length and result
loop_length = max(visited.values()) + 1
furthest_dist = loop_length // 2

print(furthest_dist)

# 6864
