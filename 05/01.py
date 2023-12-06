#! /usr/bin/env python3
import re

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

groups = [x.strip().split('\n') for x in data.split('\n\n')]

# ==== SOLUTION ====

seeds = [int(x) for x in groups[0][0].split(': ')[1].split()]


title_ranges = {}
for group in groups[1:]:
    title = re.split('\s+', group[0])[0]
    title_ranges[title] = [
        [int(x) for x in rng.split()] for rng in group[1:]]

min_seed = max(seeds)
for seed in seeds:
    for title in title_ranges.keys():
        for range in title_ranges[title]:
            dest, src, length = range
            if seed >= src and seed < src + length:
                seed = dest + (seed-src)
                break
    min_seed = min(seed, min_seed)

print(min_seed)
# 346433842
