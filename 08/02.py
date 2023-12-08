#! /usr/bin/env python3
import re
import math
from functools import reduce

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

left_right_pattern = [(0 if x == 'L' else 1) for x in rows[0]]
left_right_pointer = 0

location_map = {}
for row in rows[2:]:
    key, left_right = row.split(" = ")
    left, right = left_right[1:-1].split(', ')
    location_map[key] = (left, right)


locations = [loc for loc in location_map.keys() if loc[2] == 'A']
cycles = []

for location in locations:
    cycle = [location]
    left_right_pointer = 0
    while location[2] != 'Z':
        left_right = left_right_pattern[left_right_pointer % len(left_right_pattern)]
        location = location_map[location][left_right]
        left_right_pointer += 1
        cycle.append(location)
    cycles.append(cycle)

def lcm(numbers):
    return reduce(lambda x, y: x * y // math.gcd(x, y), numbers)

# (cycle length - 1) = number of steps
steps_to_align = lcm([len(cycle)-1 for cycle in cycles])
print(steps_to_align)

# 13740108158591
