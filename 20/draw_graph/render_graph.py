#! /usr/bin/env python3

# ==== INPUT ====

INPUT = '../input.txt'
# INPUT = '../example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

# PARSE INPUT

MOD_BROADCAST   = 'b'
MOD_FLIPFLOP    = '%'
MOD_CONJUNCTION = '&'

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

    if src_type == MOD_BROADCAST:
        broadcast_outputs = dests

    elif src_type == MOD_FLIPFLOP:
        flip_flops[src_name] = [LOW, dests]

    elif src_type == MOD_CONJUNCTION:
        conjuctions[src_name] = [dict(), dests]

# populate conjunction dictionaries (for each flip flop, no conjunctions needed)
for key in flip_flops.keys():
    _, dests = flip_flops[key]
    for dest in dests:
        if dest in conjuctions:
            conjuctions[dest][0][key] = LOW

def create_dot_script(flip_flops, conjuctions, broadcast_outputs):
    dot_script = "digraph G {\n"

    # button and broadcaster
    dot_script += "button [shape=rectangle, style=filled, color=green];\n"
    dot_script += "broadcaster [shape=box, style=filled, color=lightblue];\n"
    dot_script += "button -> broadcaster;\n"

    # flip flops
    for ff in flip_flops:
        dot_script += f"{ff} [shape=circle];\n"

    # conjunctions
    for conj in conjuctions:
        dot_script += f"{conj} [shape=diamond];\n"

    # edges:
    # - from broadcaster
    for dest in broadcast_outputs:
        dot_script += f"broadcaster -> {dest};\n"

    # - from flip flops
    for ff, (_, dests) in flip_flops.items():
        for dest in dests:
            dot_script += f"{ff} -> {dest};\n"

    # - from conjunctions
    for conj, (_, dests) in conjuctions.items():
        for dest in dests:
            dot_script += f"{conj} -> {dest};\n"

    dot_script += "}"
    return dot_script

# Create the DOT script
dot_script = create_dot_script(flip_flops, conjuctions, broadcast_outputs)

# Save the DOT script to a file
with open('network_graph.dot', 'w', encoding='UTF-8') as file:
    file.write(dot_script)

print("DOT script created and saved to 'network_graph.dot'")

# then run
# dot -Tpng network_graph.dot -o network_network.png
# code network_network.png
