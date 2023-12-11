#! /usr/bin/env python3
import numpy as np
import itertools

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

GRID = np.array([list(row.strip()) for row in data.split('\n')[:-1]])

# ==== SOLUTION ====

def double_empty_row_col(grid):
    new_rows = []
    for row in grid:
        new_rows.append(row)
        if np.all(row == '.'):
            new_rows.append(row)

    new_cols = []
    for col in np.array(new_rows).T:
        new_cols.append(col)
        if np.all(col == '.'):
            new_cols.append(col)

    grid = np.array(new_cols).T
    return grid

def manhattan(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def get_galaxy_pair_dists(arr):
    hash_coords = list(zip(*np.where(arr == '#')))
    pairs = []
    for a, b in itertools.combinations(hash_coords, 2):
        pairs.append((a, b, manhattan(a, b)))
    return pairs

new_grid = double_empty_row_col(GRID)
pair_dists = get_galaxy_pair_dists(new_grid)

total_dists = sum([dist for _, _, dist in pair_dists])
print(total_dists)

# 9947476
