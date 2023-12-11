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
    x, y = start_pos
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

# return the set of values in the loop containing the given start coordinate
def find_loop(start_coord):
    queue, visited = deque([(start_coord, 0)]), {} # (x, y): dist
    while queue:
        (x, y), dist = queue.pop()
        visited[(x, y)] = dist

        possible_steps = get_possible_steps((x, y))

        for _, (new_x, new_y), _ in possible_steps:
            if (new_x, new_y) not in visited:
                queue.append(((new_x, new_y), dist + 1))

    return visited

# flood fill outside of the loop, from the top-left of the border
def fill_outside_of_loop(loop, fill_char='O'):
    def flood_fill(x, y):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited or GRID[cy][cx] != 'I':
                continue
            GRID[cy][cx] = fill_char
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < len(GRID[0]) and 0 <= ny < len(GRID):
                    stack.append((nx, ny))

    visited = set(loop)
    exterior_point = (0, 0)
    flood_fill(*exterior_point)

# determine start position value
# - use equivalent char for 'S' in mapping
s_index = np.where(GRID == 'S')
initial_start  = (s_index[1][0], s_index[0][0])

START_CHAR = get_starting_char(initial_start)
valid_steps['S'] = valid_steps[START_CHAR]

# expand the entire grid to ensure an unfilled border
new_grid = np.full((GRID.shape[0] + 2, GRID.shape[1] + 2), '.')
new_grid[1:-1, 1:-1] = GRID
GRID = new_grid

# double the number of rows and columns (insert blank rows/cols)
# (the ensures that 0-width gaps become flood-fillable)
new_grid = np.full((GRID.shape[0] * 2, GRID.shape[1] * 2), '.')
for i in range(GRID.shape[0]):
    for j in range(GRID.shape[1]):
        new_grid[i * 2, j * 2] = GRID[i, j]
GRID = new_grid

# find new start position after expanding
s_index = np.where(GRID == 'S')
START_POS  = (s_index[1][0], s_index[0][0])

GRID[START_POS[1]][START_POS[0]] = START_CHAR

# fill in gaps introduced by new rows/columns,
# by extrapolating horiztonal/verticals with '-' and '|'
for y in range(1, GRID.shape[0]-1, 2):
    for x in range(GRID.shape[1]):
        up   = GRID[y-1][x]
        down = GRID[y+1][x]
        if 'down' in valid_steps[up] and 'up' in valid_steps[down]:
            GRID[y][x] = '|'

for x in range(1, GRID.shape[1]-1, 2):
    for y in range(GRID.shape[0]):
        left  = GRID[y][x-1]
        right = GRID[y][x+1]
        if 'right' in valid_steps[left] and 'left' in valid_steps[right]:
            GRID[y][x] = '-'

main_loop = find_loop(START_POS)

# set every non-loop cell to filled (I, 'In')
for y in range(len(GRID)):
    for x in range(len(GRID[0])):
        if (x, y) not in main_loop:
            GRID[y][x]  = 'I'

# fill everything outside of loop (O, 'Out')
fill_outside_of_loop(main_loop)

# delete added rows and cols
# (new border doesn't affect count, so is ignored)
for index in range(GRID.shape[0] - 1, -1, -2):
    GRID = np.delete(GRID, index, axis=0)  # Delete row
for index in range(GRID.shape[1] - 1, -1, -2):
    GRID = np.delete(GRID, index, axis=1)  # Delete column

# count number of of filled cells in original grid
count_i_cells = np.sum(GRID == 'I')
print(count_i_cells)

# 349
