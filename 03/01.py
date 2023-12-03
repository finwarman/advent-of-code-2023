#! /usr/bin/env python3
import re
import math
import numpy as np

# ==== INPUT ====

def load_input():
    INPUT = 'input.txt'
    with open(INPUT, 'r', encoding='UTF-8') as file:
        data = file.read()

    rows = [row.strip().replace('.', ' ') for row in data.split('\n')[:-1]]
    return rows

# ==== SOLUTION ====

# find position (row, col, length) of numbers in grid
def find_matches(array, regex):
    matches = []
    for i, text in enumerate(array):
        for match in regex.finditer(text):
            start_index = match.start()
            match_length = match.end() - start_index
            number = int(match.group())
            matches.append((i, start_index, match_length, number))
    return matches

def select_squares_with_padding(array, matches):
    padded_array = np.pad(
        array, pad_width=1, mode='constant', constant_values=' ',
    )

    squares = []
    for (row, col, length, _) in matches:
        start_row = row
        end_row = row + 2
        start_col = col
        end_col = col + length + 1

        square = padded_array[start_row:end_row+1, start_col:end_col+1]
        squares.append(square)

    return squares

if __name__ == "__main__":
    rows = load_input()

    num_re = re.compile(r'\b\d+\b')
    matches = find_matches(rows, num_re)

    array = np.array([list(row) for row in rows])
    squares = select_squares_with_padding(array, matches)

    total = 0
    for i, square in enumerate(squares):
        flat_string = ''.join(map(str, square.ravel()))
        if re.search(r'[^0-9 ]', flat_string) is not None:
            _, _, _, number = matches[i]
            total += number

    print(total)
    # 528819
