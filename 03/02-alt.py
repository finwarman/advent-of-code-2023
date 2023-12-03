#! /usr/bin/env python3
import re
import math
import numpy as np
from collections import defaultdict

# ==== INPUT ====

def load_input():
    INPUT = 'input.txt'
    with open(INPUT, 'r', encoding='UTF-8') as file:
        data = file.read()

    rows = [list(row.strip().replace('.', ' ')) for row in data.split('\n')[:-1]]
    return rows

# ==== SOLUTION ====

num_re = re.compile(r'\b\d+\b')

# check if any of a number is within range of a gear coordinate
def is_within_distance(start_coord, length, target_coord):
    y1, x1 = start_coord
    y2, x2 = target_coord

    if abs(y2 - y1) > 1 or abs(x1 - x2) > 3:
        return False

    # check points along length in x-axis, at [y-1, y, y+1]
    for i in range(length):
        for dy in [-1, 0, 1]:
            if math.sqrt((x2 - (x1 + i))**2 + (y2 - (y1 + dy))**2) <= 1:
                return True

    return False

# find (row, col, length, value) of numbers in grid
def find_numbers(arr, regex):
    matches = []
    for row, text in enumerate(arr):
        for match in regex.finditer(''.join(text)):
            start_index  = match.start()
            match_length = match.end() - start_index
            matches.append((row, start_index, match_length, int(match.group())))
    return matches

if __name__ == "__main__":
    grid = np.array(load_input())

    potential_gears = [tuple(g) for g in zip(*np.where(grid == '*'))]
    numbers = find_numbers(grid, re.compile(r'\d+'))

    # for each potential gear, get list of adjacent numbers
    gear_neighbours = defaultdict(list)
    for gear in potential_gears:
        for number in numbers:
            if len(gear_neighbours[gear]) > 2:
                break
            n_row, n_col, n_len, n_val = number
            if is_within_distance((n_row, n_col), n_len, gear):
                gear_neighbours[gear].append(n_val)

    TOTAL = sum(np.prod(nums) for nums in gear_neighbours.values() if len(nums) == 2)

    print(TOTAL)
    # 80403602
