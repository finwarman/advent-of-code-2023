#! /usr/bin/env python3
import re

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

print(sum(
    int(f'{r[0]}{r[-1]}') for r in (re.sub(r'[a-z]','', row) for row in rows)
))

# 54159
