#! /usr/bin/env python3
# %%

import numpy as np
import string
from itertools import product

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

# give each cube a unique ID, for fun
def id_generator():
    letters = string.ascii_uppercase
    sequence_length = 1
    while True:
        for ids in product(letters, repeat=sequence_length):
            yield ''.join(ids)
        sequence_length += 1
gen = id_generator()

# { 'A': (start(x,y,z), end(x,y,z)), ... }
CUBES = {}

for row in rows:
    start, end = row.split('~')
    start = tuple(int(x) for x in start.split(','))
    end = tuple(int(x) for x in end.split(','))

    cube_line = tuple((start, end))
    id = next(gen)
    CUBES[id] = cube_line

CUBE_NAMES = list(sorted(CUBES.keys()))

# Determine gird bounds

MAX_X = max(max(x[0][0], x[1][0]) for x in CUBES.values()) + 1
MAX_Y = max(max(x[0][1], x[1][1]) for x in CUBES.values()) + 1
MAX_Z = max(max(x[0][2], x[1][2]) for x in CUBES.values()) + 1

# Initialize the 3D grid with empty strings
cube = np.full((MAX_X+1, MAX_Y+1, MAX_Z+1), '', dtype=object)

# Populate the 3D grid with cube names
for name in CUBE_NAMES:
    (lx, ly, lz), (hx, hy, hz) = CUBES[name]
    for x in range(lx, hx + 1):
        for y in range(ly, hy + 1):
            for z in range(lz, hz + 1):
                cube[x][y][z] = name

# Simulate falling bricks
something_fell = True
while something_fell:
    something_fell = False
    for name, ((lx, ly, lz), (hx, hy, hz)) in CUBES.items():
        # check if the bottom of brick can fall
        if lz > 0 and all(cube[x][y][lz-1] == '' for x in range(lx, hx+1) for y in range(ly, hy+1)):
            # update the entire brick to fall
            something_fell = True
            # clear the current position of the brick
            for x in range(lx, hx+1):
                for y in range(ly, hy+1):
                    for z in range(lz, hz+1):
                        cube[x][y][z] = ''
            # move the entire brick down in z-axis
            for x in range(lx, hx+1):
                for y in range(ly, hy+1):
                    for z in range(lz-1, hz):
                        cube[x][y][z] = name

            CUBES[name] = ((lx, ly, lz-1), (hx, hy, hz-1))

# Build a 'supports' map (directly above/below)
SUPPORTED = {name: set() for name in CUBE_NAMES}
SUPPORTS = {name: set() for name in CUBE_NAMES}

for x in range(MAX_X):
    for y in range(MAX_Y):
        # get vertically above / below
        for z in range(1, MAX_Z):
            above = cube[x][y][z]
            below = cube[x][y][z-1]
            if above and below and (above != below):
                SUPPORTS[below].add(above)
                SUPPORTED[above].add(below)

# Determine deletable bricks
deletable_count = 0

for name in CUBE_NAMES:
    can_be_deleted = True
    non_supported_bricks = []

    for supported_brick in SUPPORTS[name]:
        # Check if the supported brick has alternative supports other than the current brick
        if len(SUPPORTED[supported_brick] - {name}) == 0:
            can_be_deleted = False
            non_supported_bricks.append(supported_brick)

    if can_be_deleted:
        deletable_count += 1

print(f"{deletable_count} bricks can be safely disintegrated.")

# 446

# %%
