#! /usr/bin/env python3

import numpy as np

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

grid = np.array([list(row.strip()) for row in data.split('\n')[:-1]])

# ==== SOLUTION ====

WIDTH, HEIGHT = len(grid[0]), len(grid)

def roll_rocks_north(grid):
    for x in range(WIDTH):
        for y in range(1, HEIGHT):
            if grid[y][x] == 'O':
                new_y = y
                while new_y > 0 and grid[new_y - 1][x] not in ('#', 'O'):
                    new_y -= 1

                if new_y != y:
                    grid[y][x], grid[new_y][x] = '.', 'O'

roll_rocks_north(grid)

y_positions = np.where(grid == 'O')[0]
total = sum(HEIGHT - y for y in y_positions)

print(total)

# 110565
