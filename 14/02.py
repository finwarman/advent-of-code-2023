#! /usr/bin/env python3

import numpy as np

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

grid = np.array([list(row.strip()) for row in data.split('\n')[:-1]])

# ==== SOLUTION ====

WIDTH, HEIGHT = len(grid[0]), len(grid)

def hash_array(arr):
    hash = ''.join(''.join(row) for row in arr)
    return hash
    # return hash(arr.copy().tobytes())

def roll_rocks(grid, direction):
    def move_rock(start, end, step, check, update):
        for pos1 in range(WIDTH):
            for pos2 in range(start, end, step):
                x, y = (pos1, pos2) if direction in ['n', 's'] else (pos2, pos1)
                if grid[y][x] == 'O':
                    new_x, new_y = x, y
                    while check(new_x, new_y):
                        new_x, new_y = update(new_x, new_y)

                    if new_x != x or new_y != y:
                        grid[y][x], grid[new_y][new_x] = '.', 'O'

    if direction == 'n':
        move_rock(1, HEIGHT, 1,
                  lambda x, y: y > 0 and grid[y - 1][x] not in ('#', 'O'),
                  lambda x, y: (x, y - 1))
    elif direction == 'e':
        move_rock(WIDTH - 2, -1, -1,
                  lambda x, y: x < WIDTH - 1 and grid[y][x + 1] not in ('#', 'O'),
                  lambda x, y: (x + 1, y))
    elif direction == 'w':
        move_rock(1, WIDTH, 1,
                  lambda x, y: x > 0 and grid[y][x - 1] not in ('#', 'O'),
                  lambda x, y: (x - 1, y))
    elif direction == 's':
        move_rock(HEIGHT - 2, -1, -1,
                  lambda x, y: y < HEIGHT - 1 and grid[y + 1][x] not in ('#', 'O'),
                  lambda x, y: (x, y + 1))


MAX_CYCLES = 1000000000

cycle_cache = {
    hash_array(grid): 0,
}

cycle_end, cycle_end = None, None

for cycle in range(1, MAX_CYCLES):
    for direction in ('n', 'w', 's', 'e'):
        roll_rocks(grid, direction)

    grid_hash = hash_array(grid)
    if grid_hash in cycle_cache:
        cycle_start = cycle_cache[grid_hash]
        cycle_end = cycle
        break
    else:
        cycle_cache[grid_hash] = cycle


if cycle_start is None or cycle_end is None:
    print("No cycle found.")
else:
    cycle_length       = cycle_end - cycle_start
    cycles_after_start = MAX_CYCLES - cycle_start
    remainder_cycles   = cycles_after_start % cycle_length

    print(f"Cycle start:  {cycle_start}")
    print(f"Cycle end:    {cycle_end}")
    print(f"Cycle length: {cycle_length}")
    print()
    print(f"Left to simulate:  {remainder_cycles}")
    print()

    for cycle in range(remainder_cycles):
        for direction in ('n', 'w', 's', 'e'):
            roll_rocks(grid, direction)

y_positions = np.where(grid == 'O')[0]
total = sum(HEIGHT - y for y in y_positions)

print(total)

# 89845
