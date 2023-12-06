#! /usr/bin/env python3
import re
import numpy as np

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

times        = [int(t) for t in [''.join(re.split(r'\s+', rows[0])[1:])]]
record_dists = [int(d) for d in [''.join(re.split(r'\s+', rows[1])[1:])]]

print(times)

winning_counts = []

for i in range(len(times)):
    time = times[i]
    record = record_dists[i]
    count = 0
    for hold_time in range(time):
        distance = hold_time * (time - hold_time)
        if distance > record:
            count += 1
    winning_counts.append(count)


print(winning_counts)
print(np.prod(winning_counts))

# 23501589
