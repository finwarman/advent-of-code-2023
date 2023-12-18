#! /usr/bin/env python3

import numpy as np

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip().split(' ') for row in data.split('\n')[:-1]]
rows = [(r[0], int(r[1])) for r in rows]

# ==== SOLUTION ====

UP,   DOWN  = (0, -1), (0, 1)
LEFT, RIGHT = (-1, 0), (1, 0)

DIR_MAP = {'U': UP, 'D': DOWN, 'L': LEFT, 'R': RIGHT}

def add(tup1, tup2):
    return (tup1[0]+tup2[0], tup1[1]+tup2[1])

border = []
pos = (0, 0)

for row in rows:
    steps = row[1]
    direction = DIR_MAP[row[0]]

    for i in range(steps):
        pos = add(pos, direction)
        border.append(pos)

seen  = set(border)
queue = [(1, 1)]
while queue:
    x, y = queue.pop()
    seen.add((x, y))

    for (dx, dy) in (UP, DOWN, LEFT, RIGHT):
        nx, ny = x+dx, y+dy
        if (nx, ny) not in seen:
            queue.append((nx, ny))

print(len(seen))

# 48400
