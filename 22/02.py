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

# Simulate falling bricks initially
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

def count_falling_bricks(cube, CUBES, brick_to_remove):
    # Create a copy of the grid and CUBES dictionary
    cube_copy = np.copy(cube)
    CUBES_copy = CUBES.copy()

    # Remove the specified brick
    (lx, ly, lz), (hx, hy, hz) = CUBES_copy.pop(brick_to_remove)
    for x in range(lx, hx + 1):
        for y in range(ly, hy + 1):
            for z in range(lz, hz + 1):
                cube_copy[x][y][z] = ''

    # Simulate falling
    fallen_bricks = set()
    something_fell = True
    while something_fell:
        something_fell = False
        for name, ((lx, ly, lz), (hx, hy, hz)) in CUBES_copy.items():
            if lz > 0 and all(cube_copy[x][y][lz-1] == '' for x in range(lx, hx+1) for y in range(ly, hy+1)):
                fallen_bricks.add(name)
                something_fell = True
                for x in range(lx, hx+1):
                    for y in range(ly, hy+1):
                        for z in range(lz, hz+1):
                            cube_copy[x][y][z] = ''
                        for z in range(lz-1, hz):
                            cube_copy[x][y][z] = name
                CUBES_copy[name] = ((lx, ly, lz-1), (hx, hy, hz-1))

    return len(fallen_bricks)

# Sum up the counts of falling bricks for each brick
total_fallen_bricks = sum(count_falling_bricks(cube, CUBES, name) for name in CUBE_NAMES)

print(f"Total falling bricks for every disintegration: {total_fallen_bricks}")

# 60287

# TODO: this could be optimised by dynamic programming / memoization up the 'chain reaction'
