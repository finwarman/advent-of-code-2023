#! /usr/bin/env python3
# %%

import numpy as np
from functools import cache

import matplotlib.pyplot as plt
from scipy.interpolate import BarycentricInterpolator


# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

GRID = np.array([list(row.strip()) for row in data.split('\n')[:-1]])
WIDTH = GRID.shape[0]

# ==== SOLUTION ====

PLOT, ROCKS = '.', '#'
UP, DOWN, LEFT, RIGHT = (0,-1),(0,1),(-1,0),(1,0)

@cache
def neighbours(point):
    unique_neighbours = set()
    x, y = point
    for dx, dy in (UP, DOWN, LEFT, RIGHT):
        nx, ny = (x + dx), (y + dy)
        if (GRID[ny % WIDTH][nx % WIDTH] == PLOT):
            unique_neighbours.add((nx, ny))
    return unique_neighbours

start_pos = tuple(np.argwhere(GRID == 'S')[0])
x, y = start_pos

GRID[y][x] = PLOT

# WIDTH = 131
# 26501365 = 26501300 + 65
# 26501300 / 131 = 202300

target_steps = 65 + (WIDTH * 2)

newton_x = []
newton_y = []

current_step_neighbours = {start_pos}
for step_no in range(1, target_steps + 1):
    new_neighbours = set()
    for (x, y) in current_step_neighbours:
        new_neighbours.update(neighbours((x, y)))
    current_step_neighbours = new_neighbours

    # each step in polynomial = (x * width) + 65
    # ([65, 196, 327])
    if (step_no) % WIDTH == 65:
        newton_x.append(step_no)
        newton_y.append(len(new_neighbours))

print("steps:", newton_x)
print("count:", newton_y)

def solve_quadratic(newton_x: list[int], newton_y: list[int], steps: int):
    """ Return the total number of reachable plots in a specified number of steps,
    by calculating the answer to the quadratic formula.
    Here we calculate the coefficients a, b and c by using three sample values.
    """
    c = newton_y[0]
    b = (4 * newton_y[1] - 3 * newton_y[0] - newton_y[2]) // 2
    a = newton_y[1] - newton_y[0] - b

    x = (steps - 65) // WIDTH # number of whole tile lengths
    # x = (steps - newton_x[0] // (newton_x[1] - newton_x[0]), in general

    return a*x**2 + b*x + c

# Example usage
ans = solve_quadratic(newton_x, newton_y, 26501365)
print(ans)

# 596857397104703

# Explanation:

# If the three samples are p0, p1, and p2.
# Each can be represented as a quadratic:
# p0 = a*0^2 + b*0 + c
# p1 = a*1^2 + b*1 + c
# p2 = a*2^2 + b*2 + c

# We can rearrange these formulae to come up with a set of equations
# to determine the coefficients a, b, and c.
# (three unknowns => three equations to combine)

# To find c, we can substitute 0 for x:
# p0 = c

# We can then substitute and combine the equations to solve for a and b:
# b = p1 - p0 - a
# a = (p2 - p1 - b) / 2

# Which gives the coefficients.
# (valid for our specific input grid, and resulting 'diamond' sizes)
# - diamonds describe how the broader repeating grid pattern grows

# The value of x is for the number of _whole_ tile lengths.
