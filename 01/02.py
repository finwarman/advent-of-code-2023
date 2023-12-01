#! /usr/bin/env python3
import re

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

total = 0

names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

for row in rows:
    for i, name in enumerate(names):
        new = name[:2] + str(i+1) + name[2:]
        row = row.replace(name, new)
    row = re.sub(r'[a-z]','', row)
    total += int(row[0]+row[-1])


print(total)

# 53866
