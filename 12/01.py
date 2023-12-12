#! /usr/bin/env python3
import re
import math
import numpy as np
from itertools import groupby, product

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip().split(' ') for row in data.split('\n')[:-1]]

springs = [list(row[0]) for row in rows]
group_sizes = [[int(x) for x in row[1].split(',')] for row in rows]

# ==== SOLUTION ====

OPERATIONAL, DAMAGED, UNKNOWN = ('.', '#', '?')

def get_all_indexes(arr, value):
    return [i for i, x in enumerate(arr) if x == value]

def is_valid(arrangement):
    group_counts = [len(list(g)) for k, g in groupby(arrangement) if k == DAMAGED]
    return group_counts == groups

def generate_combinations(length):
    return [''.join(p) for p in product((OPERATIONAL, DAMAGED), repeat=length)]

def valid_replacements(springs, replacements, replace_indexes):
    count = 0
    for replacement in replacements:
        for i, index in enumerate(replace_indexes):
            springs[index] = replacement[i]
        if is_valid(springs):
            count += 1
    return count

rows = []
for i, row in enumerate(springs):
    groups = group_sizes[i]
    unknown_indices = get_all_indexes(row, UNKNOWN)
    unknown_count = len(unknown_indices)

    rows.append((row, groups, unknown_count, unknown_indices))

total = 0
for row in rows:
    springs, groups, unknown_count, unknown_indices = row
    replace_combos = generate_combinations(unknown_count)

    valid_count = valid_replacements(springs, replace_combos, unknown_indices)
    total += valid_count

print(total)

# 7047

# TODO: this is very slow!
