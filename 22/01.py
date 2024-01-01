#! /usr/bin/env python3
# %%

from collections import defaultdict
import re
import math


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

    # if can_be_deleted:
    #     if SUPPORTS[name]:
    #         supported_bricks_str = ", ".join(sorted(SUPPORTS[name]))
    #         print(f"Brick {name} can be disintegrated; the bricks above it ({supported_bricks_str}) would still be supported by other bricks.")
    #     else:
    #         print(f"Brick {name} can be disintegrated; it does not support any other bricks.")
    # else:
    #     if non_supported_bricks:
    #         non_supported_bricks_str = ", ".join(sorted(non_supported_bricks))
    #         print(f"Brick {name} cannot be disintegrated safely; if it were disintegrated, bricks {non_supported_bricks_str} would both fall.")
    #     else:
    #         print(f"Brick {name} cannot be disintegrated safely; it does not have any supporting bricks.")

print(f"\nSo, in this example, {deletable_count} bricks can be safely disintegrated.")

# 446

# Plotting:

#%%

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import matplotlib.patches as mpatches

def draw_cube(ax, center, size=1, color='blue', alpha=0.3):
    # Define the vertices of a unit cube
    r = size / 2.0
    x, y, z = center
    vertices = np.array([[x - r, y - r, z - r],
                         [x + r, y - r, z - r],
                         [x + r, y + r, z - r],
                         [x - r, y + r, z - r],
                         [x - r, y - r, z + r],
                         [x + r, y - r, z + r],
                         [x + r, y + r, z + r],
                         [x - r, y + r, z + r]])

    # Generate the list of sides' polygons of our cube
    faces = [[vertices[i] for i in [0, 1, 2, 3]],
             [vertices[i] for i in [4, 5, 6, 7]],
             [vertices[i] for i in [0, 3, 7, 4]],
             [vertices[i] for i in [1, 2, 6, 5]],
             [vertices[i] for i in [2, 3, 7, 6]],
             [vertices[i] for i in [0, 1, 5, 4]]]

    # Plot the cube
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='r', alpha=alpha))

# Assuming 'cube' is your 3D grid with cube names
unique_names = np.unique(cube[cube != ''])  # Get unique non-empty cube names
colors = plt.cm.jet(np.linspace(0, 1, len(unique_names)))  # Generate distinct colors
color_map = dict(zip(unique_names, colors))  # Map cube names to colors

plt.rcParams["figure.figsize"] = [8.00, 5.00]
plt.rcParams["figure.autolayout"] = True
fig = plt.figure(dpi=150)
ax = fig.add_subplot(111, projection='3d')

# Iterate through the cube grid and draw a cube at each point
for x in range(cube.shape[0]):
    for y in range(cube.shape[1]):
        for z in range(cube.shape[2]):
            name = cube[x, y, z]
            if name:  # If the cell is not empty
                draw_cube(ax, (x, y, z), size=1, color=color_map[name], alpha=0.5)

# Set the aspect ratio
max_range = np.array([cube.shape[0], cube.shape[1], cube.shape[2]]).max() / 3.0

mid_x = (cube.shape[0]) / 2.0
mid_y = (cube.shape[1]) / 2.0
mid_z = (cube.shape[2]) / 2.0

ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

# Adjust the view
ax.view_init(elev=30, azim=-50)  # Example angles

# Create legend entries
legend_entries = [mpatches.Patch(color=color_map[name], label=name) for name in unique_names]
ax.legend(handles=legend_entries)

plt.show()


# %%
