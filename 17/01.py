#! /usr/bin/env python3

import numpy as np
from heapq import heappush, heappop

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

GRID = np.array([[int(x) for x in list(r)]
                 for row in data.split('\n') if (r := row.strip())])
WIDTH, HEIGHT = GRID.shape

# ==== SOLUTION ====

UP,   DOWN  = (0, -1), (0, 1)
LEFT, RIGHT = (-1, 0), (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
OPPOSITES  = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

GOAL_POSITION = (WIDTH-1, HEIGHT-1)

def get_neighbours(block):
    x, y, curr_dir, step_count = block
    neighbours = []

    # current direction only valid if we've been on it for less than 3 steps
    if step_count < 3:
        new_x, new_y = x + curr_dir[0], y + curr_dir[1]
        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
            neighbours.append((new_x, new_y, curr_dir, step_count + 1))

    # add all other (non-current) directions, and prevent backtracking
    for dir in DIRECTIONS:
        if dir != curr_dir and dir != OPPOSITES[curr_dir]:
            new_x, new_y = (x + dir[0], y + dir[1])
            if (0 <= new_x < WIDTH) and (0 <= new_y < HEIGHT):
                neighbours.append((new_x, new_y, dir, 1))

    return neighbours

def dijkstra(grid, start_dir=RIGHT):
    start = (0, 0, start_dir, 1)
    open_set = []
    heappush(open_set, (0, start))
    costs = {start: 0}

    while open_set:
        cost, block = heappop(open_set)
        x, y, curr_dir, step_count = block

        if (x, y) == GOAL_POSITION:
            return cost

        for neighbour in get_neighbours(block):
            nx, ny, n_dir, n_step_count = neighbour
            new_cost = cost + grid[ny, nx]

            if neighbour not in costs or new_cost < costs[neighbour]:
                costs[neighbour] = new_cost
                heappush(open_set, (new_cost, neighbour))

    return None

least_heat_loss = dijkstra(GRID)

if least_heat_loss is not None:
    print(least_heat_loss)
else:
    print("No path found")


# 1076
