#! /usr/bin/env python3
import re
import numpy as np

# ==== INPUT ====

def load_input():
    INPUT = 'input.txt'
    with open(INPUT, 'r', encoding='UTF-8') as file:
        data = file.read()

    return [row.strip().replace('.', ' ') for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

# find (row, col, length, value) of numbers in grid
def find_matches(arr, regex):
    matches = []
    for row, text in enumerate(arr):
        for match in regex.finditer(text):
            start_index  = match.start()
            match_length = match.end() - start_index
            matches.append((row, start_index, match_length, int(match.group())))
    return matches

# get subarrays with 1-char border around entire all numbers
def select_squares_with_padding(arr, num_matches):
    padded_array = np.pad(arr, pad_width=1, constant_values=' ')
    sub_squares = []
    for (row, col, length, _) in num_matches:
        start_row, end_row = row, (row + 2)
        start_col, end_col = col, (col + length + 1)

        sqr = padded_array[start_row:end_row+1, start_col:end_col+1]
        sub_squares.append(sqr)
    return sub_squares

if __name__ == "__main__":
    ROWS  = load_input()
    TOTAL = 0

    # find position, length, and a value of all numbers
    numbers = find_matches(ROWS, re.compile(r'\d+'))

    # get containing areas for all numbers
    array = np.array([list(row) for row in ROWS])
    squares = select_squares_with_padding(array, numbers)

    # sum all numbers which have a 'symbol' in their containing area
    for i, square in enumerate(squares):
        FLAT_STR = ''.join(map(str, square.ravel()))
        if re.search(r'[^0-9 ]', FLAT_STR) is not None:
            _, _, _, number = numbers[i]
            TOTAL += number

    print(TOTAL)
    # 528819
