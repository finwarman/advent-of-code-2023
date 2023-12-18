#! /usr/bin/env python3

from shapely.geometry import Polygon, LinearRing

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

def times(tup1, x):
    return (tup1[0] * x, tup1[1] * x)

pos = (0, 0)
corner_points = [pos]

for row in rows:
    steps = row[1]
    direction = DIR_MAP[row[0]]

    pos = add(pos, times(direction, steps))
    corner_points.append(pos)

polygon = Polygon(LinearRing(corner_points))
full_polygon = polygon.buffer(+0.5, join_style='mitre')

area = int(full_polygon.area)

print(area)

# 48400

# Bonus: render the polygon

# import matplotlib.pyplot as plt

# x, y = full_polygon.exterior.xy

# # Create a plot
# plt.figure()
# plt.plot(x, y)

# plt.gca().invert_yaxis()

# # Set labels and title, if desired
# plt.xlabel('X Coordinate')
# plt.ylabel('Y Coordinate')
# plt.title('Polygon Points')

# # Show the plot
# plt.show()
