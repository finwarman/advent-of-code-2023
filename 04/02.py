#! /usr/bin/env python3
import re
import math
import numpy as np

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [re.split(r'\s+\|\s+', re.split(r':\s+', row.strip())[1])
        for row in data.split('\n')[:-1]]
CARDS = len(rows)

# ==== SOLUTION ====

# map: card numbers -> matching number count
winning_counts = np.zeros(CARDS, dtype=int)

# populate match count map
for card_no, (winning, numbers) in enumerate(rows):
    winning = set(int(x) for x in re.split(r'\s+', winning))
    numbers = set(int(x) for x in re.split(r'\s+', numbers))
    win_count = len(set.intersection(winning, numbers))
    winning_counts[card_no] = win_count

# pre-compute range map for adding back to stack
range_map = [list(range(card+1, min(card+1+winning_counts[card], CARDS)))
             for card in range(CARDS)]

# resolve card counts
TOTAL = 0
stack = list(range(CARDS))
while stack:
    TOTAL += 1
    card = stack.pop()
    stack.extend(range_map[card])

print(TOTAL)

# 5132675
