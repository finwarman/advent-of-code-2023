#! /usr/bin/env python3

from shapely.geometry import Polygon

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
corner_points = [pos]

for row in rows:
    steps     = int(row[0], 16)
    direction = DIR_MAP[row[1]]

    pos = add(pos, times(direction, steps))
    corner_points.append(pos)

polygon = Polygon(corner_points)
full_polygon = polygon.buffer(+0.5, join_style='mitre')

area = int(full_polygon.area)

print(area)

# 72811019847283
