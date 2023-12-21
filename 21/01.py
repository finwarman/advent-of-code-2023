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

PLOT, ROCKS = '.', '#'
UP, DOWN, LEFT, RIGHT = (0,-1),(0,1),(-1,0),(1,0)

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

start_pos = (np.array(np.where(GRID=='S')).T)[0][::-1]
x, y = start_pos

GRID[y][x] = PLOT

TARGET_STEPS = 64

neighbour_map = {(x, y): neighbours((x, y))}
step_count, candidates = 0, {(x, y)}

for step_no in range(TARGET_STEPS):
    new_neighbours = set()
    for (x, y) in candidates:
        if (x, y) in neighbour_map:
            new_neighbours.update(neighbour_map[(x, y)])
        else:
            new_neighbours.update(neighbours((x, y)))

    candidates = new_neighbours
    step_count = len(new_neighbours)

print(step_count)

# 3617
