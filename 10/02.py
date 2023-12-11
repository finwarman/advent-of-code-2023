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
    '.': (),
    '|': ('up',   'down'  ),
    '-': ('left', 'right' ),
    'L': ('up',   'right' ),
    'J': ('up',   'left'  ),
    '7': ('down', 'left'  ),
    'F': ('down', 'right' ),

    # S = F
    # 'S': ('down', 'right' ),
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


# TODO: add a border to the grid
# Also, expand it in each direction to fill 'between the pipes'

# if either way is '-' or '|' then use that to fill the gap
# TODO: later delete these columns

new_grid = np.full((GRID.shape[0] + 2, GRID.shape[1] + 2), '.')
new_grid[1:-1, 1:-1] = GRID
GRID = new_grid


# New grid with double the rows and columns
new_grid = np.full((GRID.shape[0] * 2, GRID.shape[1] * 2), '.')

# Copy the original grid's contents into the new grid
for i in range(GRID.shape[0]):
    for j in range(GRID.shape[1]):
        new_grid[i * 2, j * 2] = GRID[i, j]

GRID = new_grid


for row in GRID:
    print(''.join(row))
print()


# find start position
s_index = np.where(GRID == 'S')
START_POS  = (s_index[1][0], s_index[0][0])

x, y = START_POS
GRID[y][x] = 'F'
# GRID[y][x] = '7'

# todo: determine start value

# Iterate over new rows/cols and fill in blank
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

for row in GRID:
    print(''.join(row))

# TODO: use 'gap joining' to fill with lines for e.g. down and up matching cells




def find_loop_for_coord(start_coord):
    x, y = start_coord
    start_char = GRID[y][x]

    visited = {}
    loop = []
    queue = deque([(start_coord, start_char, 0)])

    first = True

    while queue:
        (x, y), char, dist = queue.popleft()
        if (x, y) not in visited:
            visited[(x, y)] = dist
            loop.append((x, y, char))

            possible_steps = get_possible_steps((x, y))
            if first:
                possible_steps = [possible_steps[0]]
                first = False

            for _, (new_x, new_y), _ in possible_steps:
                if (new_x, new_y) not in visited:
                    queue.append(((new_x, new_y), GRID[new_y][new_x], dist + 1))
    return loop

main_loop = find_loop_for_coord(START_POS)

# assign number to loop
# for pos in main_loop:
#     x, y, char = pos
#     GRID[y][x] = 'A'
#     print(pos)
loop_pos = set([(x, y) for x, y, char in main_loop])

for y in range(len(GRID)):
    for x in range(len(GRID[0])):
        if (x, y) not in loop_pos:
            GRID[y][x]  = ' '

for row in GRID:
    print(''.join(row))

#  find all loops, and which loops each coord belong to

# remove all 'junk' not in loops

# todo:
# get all loops
# determine fill in the flood fill and remove the inner rings
# starting with smaller rings?

def mark_outside_of_loop(grid, loop):
    def flood_fill(x, y):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited or grid[cy][cx] != ' ':
                continue
            grid[cy][cx] = 'O'
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                    stack.append((nx, ny))

    visited = set(loop)
    exterior_point = (0, 0)
    flood_fill(*exterior_point)

mark_outside_of_loop(GRID, loop_pos)
for row in GRID:
    print(''.join(row))
print()

#  delete added rows and cols
# Delete the new columns and rows
for index in range(GRID.shape[0] - 1, -1, -2):
    GRID = np.delete(GRID, index, axis=0)  # Delete row
for index in range(GRID.shape[1] - 1, -1, -2):
    GRID = np.delete(GRID, index, axis=1)  # Delete column


# Print the reverted grid
for row in GRID:
    print(''.join(row))


count_i_cells = np.sum(GRID == ' ')
print("Number of empty cells:", count_i_cells)


# 349
