#! /usr/bin/env python3
import re
import math
import numpy as np
from collections import defaultdict
from collections import deque

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

GRID = np.array([list(row.strip()) for row in data.split('\n')[:-1]])

# ==== SOLUTION ====

# get valid chars in each direction
valid_direction_chars = {
    'up':    ('|', '7', 'F'),
    'down':  ('|', 'L', 'J'),
    'left':  ('-', 'L', 'F'),
    'right': ('-', '7', 'J'),
}
# map current char to possible directions
valid_steps = {
    '|': ('up',   'down'  ),
    '-': ('left', 'right' ),
    'L': ('up',   'right' ),
    'J': ('up',   'left'  ),
    '7': ('down', 'left'  ),
    'F': ('down', 'right' ),
}
# map direction to (dx, dy) offset
offsets = {
    'up':    ( 0, -1),
    'down':  ( 0,  1),
    'left':  (-1,  0),
    'right': ( 1,  0),
}
opposites = {
    'up':    'down' ,
    'down':  'up'   ,
    'left':  'right',
    'right': 'left' ,
}

# add tuples (e.g. x,y + offset)
def add(tuple_a, tuple_b):
    return (tuple_a[0]+tuple_b[0], tuple_a[1]+tuple_b[1])

def get_neighbours(position):
    return {
        'up':    add(position, offsets['up']),
        'down':  add(position, offsets['down']),
        'left':  add(position, offsets['left']),
        'right': add(position, offsets['right']),
    }

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

# find start position
s_index = np.where(GRID == 'S')
START_POS  = (s_index[1][0], s_index[0][0])
START_CHAR = 'F'

x, y = START_POS
GRID[y][x] = START_CHAR


visited = {}
queue = deque([(START_POS, START_CHAR, 0)])  # (x, y), char, dist
max_dist = 0

while queue:
    (x, y), current_char, dist = queue.popleft()
    if (x, y) not in visited:
        visited[(x, y)] = dist

        possible_steps = get_possible_steps((x, y))
        if (x, y) == START_POS:
            possible_steps = [possible_steps[1]]

        for direction, (new_x, new_y), new_char in possible_steps:
            if (new_x, new_y) not in visited:
                queue.append(((new_x, new_y), GRID[new_y][new_x], dist + 1))

print((max(visited.values()) + 1) // 2)

# 6864
