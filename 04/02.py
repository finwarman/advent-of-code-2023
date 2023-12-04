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

# map: card numbers -> number of 'hits'
card_score_counts = np.zeros(CARDS, dtype=int)

# resolve card counts
stack = list(range(CARDS))
while stack:
    card = stack.pop()
    card_score_counts[card] += 1
    wins = winning_counts[card]
    if wins:
        to_check = [x for x in range(card+1, min(CARDS, card+wins)+1)]
        stack.extend(to_check)

TOTAL = sum(card_score_counts)

print(TOTAL)

# 5132675
