#! /usr/bin/env python3
import re
import numpy as np
import math

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

time_input  = [int(t) for t in [''.join(re.split(r'\s+', rows[0])[1:])]][0]
record_dist = [int(d) for d in [''.join(re.split(r'\s+', rows[1])[1:])]][0]

# use quadratic formula to find bounds
# equation -x^2 + Tx - record = 0
# (where x is the 'hold time', 'T' is the total time (constant))
def find_bounds(time, record):
    # coefficients
    a, b, c = -1, time, -record
    discriminant = b**2 - 4*a*c

    # calculate roots
    root1 = (-b + math.sqrt(discriminant)) / (2*a)
    root2 = (-b - math.sqrt(discriminant)) / (2*a)

    # get solutions counts
    lower_bound = math.ceil(min(root1, root2))
    upper_bound = math.floor(max(root1, root2))

    return upper_bound - lower_bound + 1

print(find_bounds(time_input, record_dist))

# 23501589
