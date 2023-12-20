#! /usr/bin/env python3

import math

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

LOW, HIGH = -1, 1
FLIP_FLOP = -1

# 'src' -> ('value', [dests] )
flip_flops = {}

# 'src' -> ({input_name: input_value}, [dests])
conjuctions = {}

# [dests]
broadcast_outputs = []

# parse rows into module types and destinations
for row in rows:
    src, dests = row.split(' -> ')
    dests = dests.split(', ')
    src_type, src_name = src[0], src[1:]

    if src_type == 'b':
        broadcast_outputs = dests

    elif src_type == '%':
        flip_flops[src_name] = [LOW, dests]

    elif src_type == '&':
        conjuctions[src_name] = [dict(), dests]

# populate conjunction dictionaries (for each flip flop, no conjunctions needed)
for key in flip_flops.keys():
    _, dests = flip_flops[key]
    for dest in dests:
        if dest in conjuctions:
            conjuctions[dest][0][key] = LOW


# todo: determine this programmatically from what feeds into 'rx'
target_highs = {
    'mm': None,
    'ff': None,
    'lh': None,
    'fk': None,
}

# for each cycle (see graph in ./draw_graph) - get the number of button presses for output to be HIGH
cycle_no = 0
while any(value is None for value in target_highs.values()):
    cycle_no += 1

    sent_pulses = {LOW: 0, HIGH: 0}
    queue = []

    # initial 'button' pulse
    sent_pulses[LOW] += 1

    # initial broadcast (to flip flops)
    for dest in broadcast_outputs:
        sent_pulses[LOW] += 1
        flip_flops[dest][0] = FLIP_FLOP * flip_flops[dest][0]
        queue.append(dest)

    # propagate through pulses (flip flops & conjunctions)
    while queue:
        src = queue.pop(0)
        if src in flip_flops:
            value, dests = flip_flops[src]
        elif src in conjuctions:
            inputs, dests = conjuctions[src]
            value = (LOW if all(x == HIGH for x in inputs.values()) else HIGH)

        for dest in dests:
            sent_pulses[value] += 1
            if dest in flip_flops:
                if value == LOW:
                    flip_flops[dest][0] = FLIP_FLOP * flip_flops[dest][0]
                    queue.append(dest)
            elif dest in conjuctions:
                # track earliest point for high output from input to 'rx'
                if value == LOW and dest in target_highs and not target_highs.get(dest):
                    target_highs[dest] = cycle_no

                conjuctions[dest][0][src] = value
                queue.append(dest)
            else:
                continue # dead end

# get lcm of cycles to overlap
aligned_cycles = math.lcm(*target_highs.values())

print(aligned_cycles)


# 14252981424240 too low
