#! /usr/bin/env python3

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [[int(x) for x in row.strip().split()] for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

def get_diffs(sequence, max_depth):
    diffs = [sequence]
    for _ in range(max_depth):
        prev_diff = diffs[-1]
        if len(prev_diff) <= 2:
            break
        next_diff = [prev_diff[i+1] - prev_diff[i] for i in range(len(prev_diff)-1)]
        diffs.append(next_diff)
    return diffs

def previous_element(sequence):
    all_diffs = get_diffs(sequence, len(sequence) - 1)

    bottom_element = 0
    for diff in reversed(all_diffs):
        bottom_element = diff[0] - bottom_element

    return bottom_element

total = 0
for row in rows:
    prev = previous_element(row)
    total += prev

print(total)

# 905
