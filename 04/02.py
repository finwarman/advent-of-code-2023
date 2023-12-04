#! /usr/bin/env python3
import re
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
winning_counts = np.ones(CARDS, dtype=int)

# determine match counts, populate hits in each range
for card_no, (winning, numbers) in enumerate(rows):
    winning = set(int(x) for x in re.split(r'\s+', winning))
    numbers = set(int(x) for x in re.split(r'\s+', numbers))
    win_count = len(set.intersection(winning, numbers))
    current_hits = winning_counts[card_no]
    # each card in the range increases by the current card's hit count
    for i in range(win_count):
        winning_counts[(card_no+1) + i] += current_hits

print(sum(winning_counts))

# 5132675
