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

NUM_REGEX = re.compile(r'\d+')

# check if any of a number is within range of a gear coordinate
def is_within_distance(start_coord, length, target_coord):
    y1, x1 = start_coord
    y2, x2 = target_coord

    if abs(y2 - y1) > 1 or abs(x1 - x2) > 3:
        return False

    # check points along the x-axis (in length), at y, y+1, and y-1
    for i in range(length):
        for dy in [0, 1, -1]:
            if math.sqrt((x2 - (x1 + i))**2 + (y2 - (y1 + dy))**2) <= 1:
                return True
    return False

# find (row, col, length, value) of numbers in a (sub-)grid
def find_numbers(arr, regex):
    matches = []
    for i, text in enumerate(arr):
        for match in regex.finditer(''.join(text)):
            start_index = match.start()
            match_length = match.end() - start_index
            number = int(match.group())
            matches.append((i, start_index, match_length, number))
    return matches

# for the area around the current gear, get the neighbouring numbers
def get_neighbour_numbers_count(grid, gear):
    row, col = gear

    # get surrounding area of gear
    start_row, end_row = row - 1, row + 2
    start_col, end_col = col - 3, col + 4
    GEAR_CENTRE = (1, 3) # relative to area

    # find potential neighbouring numbers
    square = grid[start_row:end_row, start_col:end_col]
    matches = find_numbers(square, NUM_REGEX)

    # determine actual neighbours
    neighbours = []
    for match in matches:
        if len(neighbours) > 2:
            break
        m_row, m_col, length, number = match
        neighbour = is_within_distance((m_row, m_col), length, GEAR_CENTRE)
        if neighbour:
            neighbours.append(number)

    return neighbours

if __name__ == "__main__":
    grid = np.array(load_input())
    potential_gears = list(zip(*np.where(grid == '*')))

    # for each potential gear get the neighbouring numbers -
    # for gears with two neighbours add the 'gear ratio' to the total
    TOTAL = 0
    for gear in potential_gears:
        neighbours = get_neighbour_numbers_count(grid, gear)
        if len(neighbours) == 2:
            TOTAL += neighbours[0] * neighbours[1]

    print(TOTAL)
    # 80403602
