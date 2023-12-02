#! /usr/bin/env python3
import re

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [re.sub(r'^Game \d+\: ', '', row.strip()) for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

POWER_TOTAL = 0

for i, row in enumerate(rows):
    totals = {'red': 0, 'green': 0, 'blue': 0}
    for r in row.split('; '):
        for part in [p.split(' ') for p in r.split(', ')]:
            count, colour = int(part[0]), part[1]
            totals[colour] = max(totals[colour], count)
    POWER_TOTAL +=  totals['red'] * totals['green'] * totals['blue']

print(POWER_TOTAL)

# 74229
