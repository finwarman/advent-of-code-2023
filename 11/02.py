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

GRAVITY_MULTIPLIER = 1_000_000

def get_empty_col_rows(grid):
    empty_rows = {i for i, row in enumerate(grid) if np.all(row == '.')}
    empty_cols = {i for i, col in enumerate(grid.T) if np.all(col == '.')}
    return empty_rows, empty_cols

# manhattan distance, accounting for 'gravitational expansion' of empty rows/cols
def get_dist(a, b, empty_rows, empty_cols):
    min_row, max_row = sorted((a[0], b[0]))
    min_col, max_col = sorted((a[1], b[1]))

    gravity_rows = sum((GRAVITY_MULTIPLIER-1) for row in empty_rows if min_row <= row < max_row)
    gravity_cols = sum((GRAVITY_MULTIPLIER-1) for col in empty_cols if min_col <= col < max_col)

    y_sum = abs(a[0] - b[0]) + gravity_rows
    x_sum = abs(a[1] - b[1]) + gravity_cols

    return x_sum + y_sum

# get the sum of distances for all pairs of galaxies
def get_galaxy_pair_dist_total(arr, empty_rows, empty_cols):
    hash_coords = list(zip(*np.where(arr == '#')))
    dist_total = sum(get_dist(a, b, empty_rows, empty_cols)
                    for a, b in itertools.combinations(hash_coords, 2))
    return dist_total

empty_rows, empty_cols = get_empty_col_rows(GRID)
total_dists = get_galaxy_pair_dist_total(GRID, empty_rows, empty_cols)

print(total_dists)

# 519939907614
