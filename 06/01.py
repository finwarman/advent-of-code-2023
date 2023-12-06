#! /usr/bin/env python3
import re
import math
import sys

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

EPS = sys.float_info.epsilon * 10

times        = [int(t) for t in re.split(r'\s+', rows[0])[1:]]
record_dists = [int(d) for d in re.split(r'\s+', rows[1])[1:]]

def find_bounds(time, record):
    # coefficients
    a, b, c = -1, time, -record
    discriminant = b**2 - 4*a*c

    # calculate roots
    root1 = ((-b + math.sqrt(discriminant)) / (2*a))
    root2 = ((-b - math.sqrt(discriminant)) / (2*a))

    # get solutions counts
    lower_bound = math.ceil(min(root1, root2) + EPS)
    upper_bound = math.floor(max(root1, root2) - EPS)

    return upper_bound - lower_bound + 1

for i, time in enumerate(times):
    print(find_bounds(time, record_dists[i]))

# 1083852
