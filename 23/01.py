#! /usr/bin/env python3

import numpy as np

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

GRID = np.array([list(row.strip()) for row in data.split('\n')[:-1]])
HEIGHT, WIDTH = GRID.shape

# ==== SOLUTION ====

PATH, FOREST, SLOPES = '.', '#', ('^', 'v', '<', '>')
DIRS = (UP, DOWN, LEFT, RIGHT) = (0, -1), (0, 1), (-1, 0), (1, 0) # (dx, dy)

SLOPE_DIRS = {slope: dir for slope, dir in zip(SLOPES, DIRS)}

START_POS  = (1, 0) # (x, y)
TARGET_POS = (WIDTH-2, HEIGHT-1)

# find the longest path, never step onto same tile twice
# if you step onto a slope tile, next step must be 'downhill'

def get_valid_neighbours(pos, seen):
    x, y = pos
    char = GRID[y][x]
    neighbours = []
    if char == PATH:
        neighbours = [(x+dx, y+dy) for (dx, dy) in DIRS]
    elif char in SLOPE_DIRS:
        dx, dy = SLOPE_DIRS[char]
        neighbours.append((x+dx, y+dy))
    valid_neighbours = []
    for neighbour in neighbours:
        nx, ny = neighbour
        if neighbour in seen:
            continue
        if nx < 0 or nx >= WIDTH:
            continue
        if ny < 0 or ny >= HEIGHT:
            continue
        if GRID[ny][nx] == FOREST:
            continue
        valid_neighbours.append(neighbour)
    return valid_neighbours

# dfs, stack: [ (position, current path length, seen positions), ]
max_length = 0
stack = [(START_POS, 0, set([START_POS]))]

while stack:
    pos, length, seen = stack.pop()
    if pos == TARGET_POS:
        max_length = max(max_length, length)

    for neighbour in get_valid_neighbours(pos, seen):
        new_seen = seen.copy()
        new_seen.add(neighbour)
        stack.append((neighbour, length + 1, new_seen))

print(max_length)

# 2178
