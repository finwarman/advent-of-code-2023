#! /usr/bin/env python3

import numpy as np
from functools import cache

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

GRID = np.array([list(row.strip()) for row in data.split('\n')[:-1]])
HEIGHT, WIDTH = GRID.shape

# ==== SOLUTION ====

PLOT, ROCKS = '.', '#'
UP, DOWN, LEFT, RIGHT = (0,-1),(0,1),(-1,0),(1,0)

@cache
def neighbours(point):
    neighbours = []
    x, y = point
    for dx, dy in (UP, DOWN, LEFT, RIGHT):
        nx, ny = x+dx, y+dy
        if  (nx >= 0 and nx < WIDTH) and \
            (ny >= 0 and ny < HEIGHT) and \
            (GRID[ny][nx] == PLOT):
                neighbours.append((nx, ny))
    return neighbours

start_pos = tuple(np.argwhere(GRID == 'S')[0])
x, y = start_pos

GRID[y][x] = PLOT

TARGET_STEPS = 64

neighbour_map = {(x, y): neighbours((x, y))}
candidates = {(x, y)}

for step_no in range(TARGET_STEPS):
    new_neighbours = set()
    for (x, y) in candidates:
        new_neighbours.update(neighbour_map.get((x, y), neighbours((x, y))))
    candidates = new_neighbours

print(len(new_neighbours))

# 3617
