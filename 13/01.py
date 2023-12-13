#! /usr/bin/env python3
import numpy as np

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()


sections = [row.strip()  for row in data.split('\n\n')]
grids = [np.array([list(row)for row in section.split('\n')]) for section in sections]

# ==== SOLUTION ====

col_count = 0
row_count = 0

for grid in grids:
    rows, cols = grid.shape
    # h_flip = np.flip(grid, axis=1)
    h_done = False

    for i in range(1, cols):
        if i > cols//2:
            window = cols-i
        else:
            window = i

        left_segment  = grid[:, i-window:i]
        right_segment = np.flip(grid[:, i:i+window], axis=1)
        if np.array_equal(left_segment, right_segment):
                col_count += i
                break

    if h_done:
        continue

    # v_flip = np.flip(grid, axis=0)
    for i in range(1, rows):
        window = min(i, rows - i)
        top_segment = grid[i-window:i, :]
        bottom_segment = np.flip(grid[i:i+window, :], axis=0)
        if np.array_equal(top_segment, bottom_segment):
            row_count += i
            break


total = col_count + (100 * row_count)
print(total)

# 33047
