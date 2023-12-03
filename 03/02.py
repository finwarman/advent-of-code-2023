#! /usr/bin/env python3
import re
import math
import numpy as np

# ==== INPUT ====

def load_input():
    INPUT = 'input.txt'
    with open(INPUT, 'r', encoding='UTF-8') as file:
        data = file.read()

    rows = [list(row.strip().replace('.', ' ')) for row in data.split('\n')[:-1]]
    return rows

# ==== SOLUTION ====

num_re = re.compile(r'\b\d+\b')

def is_within_distance(start_coord, length, target_coord):
    x1, y1 = start_coord
    x2, y2 = target_coord

    # check points along the x-axis (in length), at y, y+1, and y-1
    for i in range(length):
        for dy in [0, 1, -1]:
            if math.sqrt((x2 - (x1 + i))**2 + (y2 - (y1 + dy))**2) <= 1:
                return True
    return False

def find_matches(array, regex):
    matches = []
    for i, text in enumerate(array):
        for match in regex.finditer(''.join(text)):
            start_index = match.start()
            match_length = match.end() - start_index
            number = int(match.group())
            matches.append((i, start_index, match_length, number))
    return matches

def get_neighbour_numbers_count(grid, gear):
    row, col = gear

    start_row = row - 1
    end_row = row + 2
    start_col = col - 3
    end_col = col + 4

    square = grid[start_row:end_row, start_col:end_col]
    matches = find_matches(square, num_re)
    neighbours = []
    for match in matches:
        m_row, m_col, length, number = match
        neighbour = is_within_distance((m_col, m_row), length, (3, 1))
        if neighbour:
            neighbours.append(number)
        if len(neighbours) > 2:
            break
    return neighbours

if __name__ == "__main__":
    grid = np.pad(
        load_input(),
        pad_width=3, mode='constant', constant_values=' ',
    )

    row_indices, col_indices = np.where(grid == '*')
    potential_gears = zip(row_indices, col_indices)

    total = 0
    for gear in potential_gears:
        neighbours = get_neighbour_numbers_count(grid, gear)
        if len(neighbours) == 2:
            gear_ratio = neighbours[0] * neighbours[1]
            total += gear_ratio

    print(total)
    # 80403602
