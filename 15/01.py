#! /usr/bin/env python3

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

input = data.strip()
steps = input.split(',')

# ==== SOLUTION ====

grand_total = 0
for step in steps:
    total = 0
    for char in step:
        total = ((total + ord(char)) * 17) % 256
    grand_total += total

print(grand_total)

# 516070
