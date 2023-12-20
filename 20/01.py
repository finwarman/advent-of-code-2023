#! /usr/bin/env python3

import json

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

# populate conjunction dictionaries (for each flip flop/conjuction dest)
for key in flip_flops.keys():
    _, dests = flip_flops[key]
    for dest in dests:
        if dest in conjuctions:
            conjuctions[dest][0][key] = LOW
# for key in conjuctions.keys():
#     _, dests = conjuctions[key]
#     for dest in dests:
#         if dest in conjuctions:
#             conjuctions[dest][0][key] = LOW

# state string to sent_pulses
states = {}
break_cycle = None
repeat_length = None
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

    # serialize state
    state = json.dumps(flip_flops, sort_keys=True) + json.dumps(conjuctions, sort_keys=True)

    # check for cycle
    if state in states:
        debug_print(f"Reached state before (currently on cycle #{cycle_no})")
        break_cycle = cycle_no
        repeat_length = cycle_no - states[state][2]  # Calculate repeat length
        break  # Exit loop since we found a cycle

    # save state with the cycle number and sent pulses counts
    states[state] = (sent_pulses[LOW], sent_pulses[HIGH], cycle_no)

    total_sent_pulses[LOW] += sent_pulses[LOW]
    total_sent_pulses[HIGH] += sent_pulses[HIGH]

# if a cycle was detected, skip repeats and calculate final values
if break_cycle is not None:
    remaining_cycles = final_cycle - break_cycle

    # total pulses for one complete loop
    loop_pulses = {
        LOW: sum(state_info[0] for state_info in states.values() if state_info[2] < repeat_length),
        HIGH: sum(state_info[1] for state_info in states.values() if state_info[2] < repeat_length)
    }

    #  getnumber of complete loops remaining and add the pulses
    complete_loops = remaining_cycles // repeat_length
    total_sent_pulses[LOW] += complete_loops * loop_pulses[LOW]
    total_sent_pulses[HIGH] += complete_loops * loop_pulses[HIGH]

    # add the pulses for the partial remaining loop (if required)
    partial_loop_cycles = remaining_cycles % repeat_length
    for cycle in range(partial_loop_cycles):
        total_sent_pulses[LOW] += states[state][0]
        total_sent_pulses[HIGH] += states[state][1]

total_low, total_high = total_sent_pulses[LOW], total_sent_pulses[HIGH]
print(f"Simulated {final_cycle} cycles:")
print(f"  Total LOW pulses:  {total_low}")
print(f"  Total HIGH pulses: {total_high}")
print(f"  Product of LOW and HIGH: {total_low * total_high}")
print()
print(f"{total_low * total_high}")


# 814934624
