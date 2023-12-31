#! /usr/bin/env python3
import numpy as np

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

data = data.replace('#', '1').replace('.', '0')
grids = [np.array([list(map(int, row)) for row in section.strip().split('\n')])
            for section in data.split('\n\n')]

# ==== SOLUTION ====

def array_flip(grid, cols):
    flip = np.flip(grid, axis=1)

    for i in range(1, cols):
        window = min(i, cols - i)
        left_segment  = grid[:, i-window:i]
        right_segment = flip[:, cols-i-window:cols-i]

        if np.all(left_segment == right_segment):
            return i
    return None

col_count, row_count = 0, 0
for grid in grids:
    rows, cols = grid.shape

    h_count = array_flip(grid, cols)
    if h_count is not None:
        col_count += h_count
        continue

    v_count = array_flip(grid.T, rows)
    if v_count is not None:
        row_count += v_count


total = col_count + (100 * row_count)
print(total)

# 33047
