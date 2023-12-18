#! /usr/bin/env python3

import numpy as np

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip().split(' ') for row in data.split('\n')[:-1]]
rows = [(r[2][2:-2], r[2][-2]) for r in rows]

# ==== SOLUTION ====

UP,   DOWN  = (0, -1), (0, 1)
LEFT, RIGHT = (-1, 0), (1, 0)

DIR_MAP = {'0': RIGHT, '1': DOWN, '2': LEFT, '3': UP}

def add(tup1, tup2):
    return (tup1[0]+tup2[0], tup1[1]+tup2[1])

def times(tup1, x):
    return (tup1[0] * x, tup1[1] * x)

pos = (0, 0)
corner_points = []

for row in rows:
    steps, direction = int(row[0], 16), DIR_MAP[row[1]]
    pos = add(pos, times(direction, steps))
    corner_points.append(pos)

def shoelace_area(points):
    points = np.array(points)
    x, y = points[:, 0], points[:, 1]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

area = shoelace_area(corner_points)
print(int(area))

# 72811019847283

# -- non-numpy version --

# def shoelace_area(points):
#     n = len(points)
#     area = 0.0

#     for i in range(n - 1):
#         x1, y1 = points[i]
#         x2, y2 = points[i + 1]
#         area += (x1 * y2) - (x2 * y1)

#     return abs(area) / 2
