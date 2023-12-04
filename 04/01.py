#! /usr/bin/env python3
import re

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [re.split(r'\s+\|\s+', re.split(r':\s+', row.strip())[1])
        for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

TOTAL = 0
for winning, numbers in rows:
    winning = set(int(x) for x in re.split(r'\s+', winning))
    numbers = set(int(x) for x in re.split(r'\s+', numbers))
    winning_count = len(set.intersection(winning, numbers))
    if winning_count:
        TOTAL += 2**(winning_count-1)

print(TOTAL)

# 21959
