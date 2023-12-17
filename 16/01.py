#! /usr/bin/env python3

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

GRID = [list(row.strip()) for row in data.split('\n') if row.strip()]
WIDTH, HEIGHT = len(GRID[0]), len(GRID)

# ==== SOLUTION ====

# (dx, dy)
UP, DOWN    = (0, -1), (0, 1)
LEFT, RIGHT = (-1, 0), (1, 0)

SEEN_BEAMS = set()
ENERGIZED_TILES = set()

REFLECT_RIGHT = {RIGHT: UP, DOWN: LEFT, LEFT: DOWN, UP: RIGHT} # /
REFLECT_LEFT  = {RIGHT: DOWN, DOWN: RIGHT, LEFT: UP, UP: LEFT} # \

def get_new_beams(beam):
    (x, y), (dx, dy) = beam
    dir = beam[1]

    next_beams = []

    x, y = (x + dx, y + dy)
    if (x < 0 or x >= WIDTH) or (y < 0 or y >= HEIGHT):
        return next_beams

    tile = GRID[y][x]

    if tile == '|' and dir in (LEFT, RIGHT):
        next_beams.append(((x, y), UP))
        next_beams.append(((x, y), DOWN))
    elif tile == '-' and dir in (UP, DOWN):
        next_beams.append(((x, y), LEFT))
        next_beams.append(((x, y), RIGHT))
    elif tile == '/':
        next_beams.append(((x, y), REFLECT_RIGHT[dir]))
    elif tile == '\\':
        next_beams.append(((x, y), REFLECT_LEFT[dir]))
    else:
        next_beams.append(((x, y), dir))

    return next_beams

start_beam = ( (-1, 0), RIGHT )

queue = [start_beam]
while queue:
    beam = queue.pop(0)
    SEEN_BEAMS.add(beam)
    ENERGIZED_TILES.add(beam[0])
    new_beams = get_new_beams(beam)
    for new_beam in new_beams:
        if new_beam not in SEEN_BEAMS:
            queue.append(new_beam)

print(len(ENERGIZED_TILES)-1)

# 8539
