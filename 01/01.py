#! /usr/bin/env python3
import re
import math

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

total = 0

for row in rows:
    row = re.sub(r'[a-z]','', row)
    number = int(f'{row[0]}{row[-1]}')
    total += number

print(total)
