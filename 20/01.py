#! /usr/bin/env python3

DEBUG = False
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

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

final_cycle = 1000

total_sent_pulses = {LOW: 0, HIGH: 0}

# press button 1000 times
for cycle_no in range(final_cycle):
    sent_pulses = {LOW: 0, HIGH: 0}
    queue = []

    # initial 'button' pulse
    sent_pulses[LOW] += 1
    debug_print("button -low-> broadcaster")

    # initial broadcast (to flip flops)
    for dest in broadcast_outputs:
        debug_print(f"broadcaster -low-> {dest}")
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
            val_str = "high" if value == HIGH else "low"
            debug_print(f"{src} -{val_str}-> {dest}")

            sent_pulses[value] += 1
            if dest in flip_flops:
                if value == LOW:
                    flip_flops[dest][0] = FLIP_FLOP * flip_flops[dest][0]
                    queue.append(dest)
            elif dest in conjuctions:
                conjuctions[dest][0][src] = value
                queue.append(dest)
            else:
                continue # dead end

    debug_print()

    total_sent_pulses[LOW] += sent_pulses[LOW]
    total_sent_pulses[HIGH] += sent_pulses[HIGH]

total_low, total_high = total_sent_pulses[LOW], total_sent_pulses[HIGH]
print(f"Simulated {final_cycle} cycles:")
print(f"  Total LOW pulses:  {total_low}")
print(f"  Total HIGH pulses: {total_high}")
print(f"  Product of LOW and HIGH: {total_low * total_high}")
print()
print(f"{total_low * total_high}")


# 814934624
