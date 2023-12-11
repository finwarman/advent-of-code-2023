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

# GRAVITY_MULTIPLIER = 2
GRAVITY_MULTIPLIER = 1_000_000

def get_empty_col_rows(grid):
    empty_rows = set()
    for i, row in enumerate(grid):
        if np.all(row == '.'):
            empty_rows.add(i)

    empty_cols = set()
    for i, col in enumerate(grid.T):
        if np.all(col == '.'):
            empty_cols.add(i)

    return empty_rows, empty_cols


def get_dist(a, b, empty_rows, empty_cols):
    row_range = set(range(*sorted((a[0], b[0]))))
    col_range = set(range(*sorted((a[1], b[1]))))

    gravity_rows = len(row_range.intersection(empty_rows)) * (GRAVITY_MULTIPLIER - 1)
    gravity_cols = len(col_range.intersection(empty_cols)) * (GRAVITY_MULTIPLIER - 1)

    y_sum = abs(a[0] - b[0]) + gravity_rows
    x_sum = abs(a[1] - b[1]) + gravity_cols

    return x_sum + y_sum

def get_galaxy_pair_dists(arr, empty_rows, empty_cols):
    hash_coords = list(zip(*np.where(arr == '#')))
    pairs = []
    for a, b in itertools.combinations(hash_coords, 2):
        pairs.append((a, b, get_dist(a, b, empty_rows, empty_cols)))
    return pairs

empty_rows, empty_cols = get_empty_col_rows(GRID)
pair_dists = get_galaxy_pair_dists(GRID, empty_rows, empty_cols)

total_dists = sum([dist for _, _, dist in pair_dists])
print(total_dists)

# 519939907614
