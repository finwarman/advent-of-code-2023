#! /usr/bin/env python3
import re

from cv2 import merge

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

groups = [x.strip().split('\n') for x in data.split('\n\n')]

# ==== SOLUTION ====

seeds = [int(x) for x in groups[0][0].split(': ')[1].split()]
seed_ranges = [(seeds[i], seeds[i]+seeds[i+1]-1) for i in range(0, len(seeds), 2)]

# parse each group into
# { title -> [(dest_hi, dest_lo), (source_hi, source_lo), ...] }
title_ranges = {}
for group in groups[1:]:
    title = re.split('\s+', group[0])[0]
    range_data = [[int(x) for x in rng.split()] for rng in group[1:]]
    ranges = [[(range[0], range[0]+range[2]-1), (range[1], range[1]+range[2]-1)] for range in range_data]
    title_ranges[title] = ranges
titles = list(title_ranges.keys())

# given a seed range and a potential mapping, return the adjust destination mapping
# if there is overlap, also return the overlap either side (or None), format:
# [(destination range), (left/original range), (right range)]
def intersect_range_with_dest_mapping(seed_range, source_range, dest_range):
    start = max(seed_range[0], source_range[0])
    end = min(seed_range[1], source_range[1])

    # if there is an intersection
    if start < end:
        # get adjusted mapping
        offset = start - source_range[0]
        mapped_start = dest_range[0] + offset
        mapped_end = dest_range[0] + offset + (end - start)
        mapped_destination = (mapped_start, mapped_end)

        # get non-intersecting parts
        non_intersecting_lo = (seed_range[0], start-1) if seed_range[0] < start else None
        non_intersecting_hi = (end + 1, seed_range[1]) if end < seed_range[1] else None

        return [mapped_destination, non_intersecting_lo, non_intersecting_hi]
    else:
        return [None, seed_range, None]

# for each mapping stage determine all possible resulting values
# (apply mappings, keep leftovers), pass these onto next stage
processing_inputs = seed_ranges
for title in titles:
    mapping = title_ranges[title]
    result = []
    while processing_inputs:
        input = processing_inputs.pop()
        intersected = False
        for i, (dest, src) in enumerate(mapping):
            new_inputs = []
            dest, left, right = intersect_range_with_dest_mapping(input, src, dest)
            if dest:
                intersected = True
                result.append(dest)
                processing_inputs.extend([x for x in [left, right] if x is not None])
                break
        if not intersected:
            result.append(input)
    processing_inputs = result

# determine minimum value in final stage output
print(min(processing_inputs)[0])

# 60294664
