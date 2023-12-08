#! /usr/bin/env python3
import re
import math

from networkx import local_constraint

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


location = 'AAA'
while location != 'ZZZ':
    left_right = left_right_pattern[left_right_pointer % len(left_right_pattern)]
    location = location_map[location][left_right]
    left_right_pointer += 1

print(left_right_pointer)

# 11309
