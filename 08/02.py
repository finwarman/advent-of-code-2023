#! /usr/bin/env python3
import math

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
    left, right = left_right[1:-1].split(', ')
    location_map[key] = (left, right)

locations = [loc for loc in location_map.keys() if loc[2] == 'A']
cycles = []

# for each starting location, get number of steps (cycle) from A->Z
for location in locations:
    counter = 0
    while location[2] != 'Z':
        left_right = lr_pattern[counter % len(lr_pattern)]
        location = location_map[location][left_right]
        counter += 1
    cycles.append(counter)

# get the lowest common multiple of all cycle lengths
steps_to_align = math.lcm(*cycles)

print(steps_to_align)

# 13740108158591
