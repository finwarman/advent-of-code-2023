#! /usr/bin/env python3
# %%

from dataclasses import dataclass
from typing import List
import numpy as np

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.strip().split('\n')]

DEBUG_MODE = ('example' in INPUT)
def debug(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)

# ==== SOLUTION ====

AREA_MIN, AREA_MAX = 7, 27
if not DEBUG_MODE:
    AREA_MIN, AREA_MAX = 200000000000000, 400000000000000

@dataclass
class Hailstone:
    id:  int
    pos: tuple[int, int, int]
    vel: tuple[int, int, int]

def within_test_area(point):
    return (AREA_MIN <= point[0] <= AREA_MAX) and (AREA_MIN <= point[1] <= AREA_MAX)

def intersect(stone1: Hailstone, stone2: Hailstone) -> (bool, str):
    (px1, py1, _), (dx1, dy1, _) = stone1.pos, stone1.vel
    (px2, py2, _), (dx2, dy2, _) = stone2.pos, stone2.vel

    # Check for parallel paths
    if dx1 * dy2 == dx2 * dy1:
        return False, "are parallel; they never intersect"

    # Calculate slopes (m1, m2) and y-intercepts (b1, b2)
    m1, m2 = None, None
    if dx1 != 0:
        m1 = dy1 / dx1
        b1 = py1 - m1 * px1

    if dx2 != 0:
        m2 = dy2 / dx2
        b2 = py2 - m2 * px2

    # Find the intersection point (x, y)
    if m1 is not None and m2 is not None:
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
    # (Unused 'inf' slop cases):
    elif m1 is None and m2 is not None:  # First line vertical
        x = px1
        y = m2 * x + b2
    elif m2 is None and m1 is not None:  # Second line vertical
        x = px2
        y = m1 * x + b1

    if not (AREA_MIN <= x <= AREA_MAX and AREA_MIN <= y <= AREA_MAX):
        return False, f"will cross outside the test area (at x={x:.3f}, y={y:.3f})"

    if not (((x > px1 and dx1 > 0) or (x < px1 and dx1 < 0))
        and ((x > px2 and dx2 > 0) or (x < px2 and dx2 < 0))):
        return False, f"crossed in the past"

    return True, f"will cross inside the test area (at x={x:.3f}, y={y:.3f})"


HAILSTONES: List[Hailstone] = []

# Parse Input
for id, row in enumerate(rows):
    pos, vel = row.split(' @ ')
    pos = tuple(int(v) for v in pos.split(', '))
    vel = tuple(int(v) for v in vel.split(', '))

    stone = Hailstone(id, pos, vel)
    HAILSTONES.append(stone)

intersecting_count = 0

# Determine intersections
for i, hailstoneA in enumerate(HAILSTONES):
    for hailstoneB in HAILSTONES[i+1:]:
        debug(f"Hailstone A: {hailstoneA.pos} @ {hailstoneA.vel}")
        debug(f"Hailstone B: {hailstoneB.pos} @ {hailstoneB.vel}")
        intersected, reason = intersect(hailstoneA, hailstoneB)
        if intersected:
            intersecting_count += 1
            debug(f"Hailstones' paths {reason}.")
        else:
            debug(f"Hailstones' paths {reason}.")
        debug()

print("Intersecting paths count (in future, within bounds):", intersecting_count)

# 16050

# %%
