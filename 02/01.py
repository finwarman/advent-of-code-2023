#! /usr/bin/env python3
import re

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [re.sub(r'^Game \d+\: ', '', row.strip()) for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

max_colours = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

VALID_IDS_SUM = 0

for i, row in enumerate(rows):
    rounds = row.split('; ')
    VALID = True
    for parts in [r.split(', ') for r in rounds]:
        totals = {'red': 0, 'green': 0, 'blue': 0}
        for part in [p.split(' ') for p in parts]:
            count, colour = int(part[0]), part[1]
            totals[colour] += count
            if totals[colour] > max_colours[colour]:
                VALID = False
                break
    if VALID:
        VALID_IDS_SUM += i + 1


print(VALID_IDS_SUM)

# 2256
