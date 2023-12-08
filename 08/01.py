#! /usr/bin/env python3

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

lr_pattern = [(0 if x == 'L' else 1) for x in rows[0]]

location_map = {}
for row in rows[2:]:
    key, left_right = row.split(" = ")
    location_map[key] = tuple(left_right[1:-1].split(', '))

location, counter = ('AAA', 0)
while location != 'ZZZ':
    left_right = lr_pattern[counter % len(lr_pattern)]
    location = location_map[location][left_right]
    counter += 1

print(counter)

# 11309
