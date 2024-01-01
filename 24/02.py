#! /usr/bin/env python3
# %%

from dataclasses import dataclass
from typing import List
import sympy as sp

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.strip().split('\n')]

# ==== SOLUTION ====

@dataclass
class Hailstone:
    id:  int
    pos: tuple[int, int, int]
    vel: tuple[int, int, int]

HAILSTONES: List[Hailstone] = []

# Parse Input
for id, row in enumerate(rows):
    pos, vel = row.split(' @ ')
    pos = tuple(int(v) for v in pos.split(', '))
    vel = tuple(int(v) for v in vel.split(', '))

    stone = Hailstone(id, pos, vel)
    HAILSTONES.append(stone)


# Determine point in time at which the first N hailstones are aligned
# and get the alignment vector, and position at t=0 (so we can snipe them all!)

# Build system of simultaneous equations (for first n hailstones):
N_STONES = 3

# Define unknowns (target)
time_symbols = ' '.join([f't{i+1}' for i in range(N_STONES+1)])
unknowns = sp.symbols('x y z dx dy dz' + time_symbols)
x, y, z, dx, dy, dz, *time = unknowns

# Build equations (e.g. for n=3, 9 equations with 9 unknowns)
equations = []
for t, stone in zip(time, HAILSTONES[:N_STONES+1]):
    pos, vel = stone.pos, stone.vel
    equations.append(sp.Eq(x + t*dx, pos[0] + t*vel[0]))
    equations.append(sp.Eq(y + t*dy, pos[1] + t*vel[1]))
    equations.append(sp.Eq(z + t*dz, pos[2] + t*vel[2]))

# Solve system of equations
solution = sp.solve(equations, unknowns).pop()

x, y, z = solution[:3]

# Get sum of x, y, z (first three unknowns)
print("x =", x)
print("y =", y)
print("z =", z)
print()
print("Total:", sum([x, y, z]))

# 669042940632377
