#! /usr/bin/env python3

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

workflows = [row.strip() for row in data.split('\n\n')[0].split('\n')]
part_rows = [row.strip() for row in data.split('\n\n')[1].split('\n')[:-1]]

# ==== SOLUTION ====

workflow_mappings = {}
parts = []

# parse workflows
for workflow in workflows:
    name, maps_str = workflow[:-1].split('{')
    mappings = []
    for map_str in maps_str.split(',')[:-1]:
        cond, dest = map_str.split(':')
        key, comp, cond = cond[0], cond[1], cond[2:]
        cond_func = eval(f"lambda stat: part['{key}'] {comp} {cond}")
        mappings.append((cond_func, dest))
    mappings.append((lambda _: True, maps_str.split(',')[-1]))
    workflow_mappings[name] = mappings

# parse parts
for part_str in part_rows:
    values = part_str[1:-1].split(',')
    part = {}
    for entry in values:
        key, val = entry.split('=')
        part[key] = int(val)
    parts.append(part)

# run workflows

total = 0
for part in parts:
    curr_stage = 'in'
    while curr_stage not in ('A', 'R'):
        workflows = workflow_mappings[curr_stage]
        for cond_func, next_stage in workflows:
            passed = cond_func(part)
            if passed:
                curr_stage = next_stage
                break

    if curr_stage == 'A':
        part_total = part['x'] + part['m'] + part['a'] + part['s']
        total += part_total

print(total)

# 367602
