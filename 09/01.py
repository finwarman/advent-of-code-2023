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

# next element is the sum of last value across diffs
def next_element(sequence):
    all_diffs = get_diffs(sequence, len(sequence) - 1)
    return sum(diff[-1] for diff in all_diffs)

total = sum([next_element(row) for row in rows])

print(total)

# 1901217887
