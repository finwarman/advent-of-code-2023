#!/usr/bin/env bash

# config
year="2023"

# place aoc 'session' cookie into '.aoc_session'
session_file=".aoc_session"
export AOC_SESSION=$(cat "$session_file")

echo "======== Advent of Code Setup ========="
echo ""

read YYYY MM DD <<<$(date +'%Y %m %d')
echo "Today is Day $DD of Advent of Code!"
echo ""

echo "Creating directory './$DD'..."
dir="$DD"
if [[ ! -d $dir ]]; then
    mkdir $dir
    echo "Created ./$DD"
else
    echo "Directory ./$dir already exists, continuing..." 1>&2
fi
echo ""

echo "Fetching todays input to ./$DD/input.txt..."
aocd > "./$DD/input.txt"
echo "Done!"
echo ""


echo "Generating Python boilerplate files"

nl=$'\\n'
read -r -d '' boilerplate <<-EOF
#! /usr/bin/env python3
import re
import math

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('$nl')[:-1]]

# ==== SOLUTION ====

total = 0

for row in rows:
    total += 1

print(total)
EOF

FILE1="./$DD/01.py"
if [ -f "$FILE1" ]; then
    echo "$FILE1 already exists, skipping."
else
    echo "Creating '$FILE1' with boilerplate"
    echo "$boilerplate" > "$FILE1"
fi
FILE2="./$DD/02.py"
if [ -f "$FILE2" ]; then
    echo "$FILE2 already exists, skipping."
else
    echo "Creating '$FILE2' with boilerplate"
    echo "$boilerplate" > "$FILE2"
fi
chmod +x "$FILE1"
chmod +x "$FILE2"
echo "(Set executable permissions)"
echo ""

echo "Opening in VS Code..."
code "./$DD/input.txt"
code "./$DD/02.py"
code "./$DD/01.py"
echo ""

number_no_leading=$(echo $DD | sed 's/^0*//')
echo "Opening today's challenge in browser...."
echo "https://adventofcode.com/$year/day/$number_no_leading"
open "https://adventofcode.com/$year/day/$number_no_leading"
echo ""

echo "Done!"
echo ""
echo "======================================"
