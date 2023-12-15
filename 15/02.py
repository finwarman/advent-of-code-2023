#! /usr/bin/env python3

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

input = data.strip().replace("-", "=")
steps = input.split(',')

# ==== SOLUTION ====

LENSES = [dict() for _ in range(256)]

def hash(string):
    total = 0
    for char in string:
        total = ((total + ord(char)) * 17) % 256
    return total

for step in steps:
    string, value = step.split('=')
    curr_lens_box = LENSES[hash(string)]
    if value:
        curr_lens_box[string] = int(value)
    else:
        curr_lens_box.pop(string, None)

focusing_power = sum(
    (i+1) * (j+1) * focal_length
    for i, box in enumerate(LENSES)
    for j, focal_length in enumerate(box.values())
)

print(focusing_power)

# 244981
