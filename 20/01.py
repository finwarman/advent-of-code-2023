#! /usr/bin/env python3

import re
import math
import json

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

MOD_BROADCAST   = 'b'
MOD_FLIPFLOP    = '%'
MOD_CONJUNCTION = '&' # NAND

LOW, HIGH = -1, 1
FLIP_FLOP, UNCHANGED = -1, 1

# 'src' -> ('value', [dests] )
# e.g.  ->  (LOW, [a, b, c])
flip_flops = {}

# 'src' -> ({input states, name: input_value}, outputs)
conjuctions = {}

broadcast_outputs = []

# parse rows
for row in rows:
    # parse module type and dests
    src, dests = row.split(' -> ')
    dests = dests.split(', ')
    src_type, src_name = src[0], src[1:]

    # get modify constants, add to map

    if src_type == MOD_BROADCAST:
        broadcast_outputs = dests

    elif src_type == MOD_FLIPFLOP:
        flip_flops[src_name] = [
            LOW, dests
        ]

    elif src_type == MOD_CONJUNCTION:
        conjuctions[src_name] = [
            dict(), dests
        ]

# populate conjunction dictionaries (for each flip flop/conjuction dest)
for key in flip_flops.keys():
    _, dests = flip_flops[key]
    for dest in dests:
        if dest in conjuctions:
            conjuctions[dest][0][key] = LOW
for key in conjuctions.keys():
    _, dests = conjuctions[key]
    for dest in dests:
        if dest in conjuctions:
            conjuctions[dest][0][key] = LOW

print(broadcast_outputs)
print()
print("Flip flops:")
print(json.dumps(flip_flops, indent=2))
print()
print("Conjuctions:")
print(json.dumps(conjuctions, indent=2))
print()

# propagate the signals

# flipflop - recieves low, it flips (also send out pulse)
#            recieved high, stays the same (doesn't send out pulse)

# 8 low, 4 high

# state string to sent_pulss
states = {}
break_cycle = None
repeat_length = None
final_cycle = 1000

total_sent_pulses = {LOW: 0, HIGH: 0}

# press button 1000 times
for cycle_no in range(final_cycle):
    sent_pulses = {
        LOW: 0,
        HIGH: 0,
    }

    queue = []

    # initial 'button' pulse
    sent_pulses[LOW] += 1
    print("button -low-> broadcaster")

    # do initial broadcast (to flip flops)
    for dest in broadcast_outputs:
        print(f"broadcaster -low-> {dest}")
        sent_pulses[LOW] += 1
        flip_flops[dest][0] = FLIP_FLOP * flip_flops[dest][0]
        queue.append(dest)

    # propagate through pulses (flip flops and conjunctions)
    while queue:
        src = queue.pop(0)
        if src in flip_flops:
            value, dests = flip_flops[src]
        elif src in conjuctions:
            inputs, dests = conjuctions[src]
            value = (LOW if all(x == HIGH for x in inputs.values()) else HIGH)
        else:
            # print(f"  [Src '{src}' dead end]")
            continue

        for dest in dests:
            val_str = "high" if value == HIGH else "low"
            print(f"{src} -{val_str}-> {dest}")

            sent_pulses[value] += 1
            if dest in flip_flops:
                if value == LOW:
                    flip_flops[dest][0] = FLIP_FLOP * flip_flops[dest][0]
                    queue.append(dest)
            elif dest in conjuctions:
                conjuctions[dest][0][src] = value
                queue.append(dest)
            else:
                # print(f"  [Dest '{dest}' dead end]")
                continue
        # todo: cycle detection

    print()
    # state = json.dumps(flip_flops, sort_keys=True) + json.dumps(conjuctions, sort_keys=True)
    # if state in states:
    #     print(f"Reached state before (currently on cycle #{cycle_no})")
    #     break_cycle = cycle_no
    #     break
    #     # skip here and finish loops
    # states[state] = (sent_pulses[LOW], sent_pulses[HIGH])
    # # print answer

    # Serialize the current state
    state = json.dumps(flip_flops, sort_keys=True) + json.dumps(conjuctions, sort_keys=True)

    # Check for cycle
    if state in states:
        print(f"Reached state before (currently on cycle #{cycle_no})")
        break_cycle = cycle_no
        repeat_length = cycle_no - states[state][2]  # Calculate repeat length
        break  # Exit loop since we found a cycle

    # Save the state with the cycle number and the sent pulses
    states[state] = (sent_pulses[LOW], sent_pulses[HIGH], cycle_no)

    # Accumulate sent pulses
    total_sent_pulses[LOW] += sent_pulses[LOW]
    total_sent_pulses[HIGH] += sent_pulses[HIGH]

print()
print(sent_pulses)
print(sent_pulses[LOW] * sent_pulses[HIGH])
print()


# If a cycle was detected
if break_cycle is not None:
    cycle_offset = (final_cycle - break_cycle) % repeat_length
    # Find the state that would be reached after the remaining cycles
    for state, info in states.items():
        if info[2] == break_cycle + cycle_offset:
            sent_pulses[LOW], sent_pulses[HIGH] = info[0], info[1]
            print(f"Final state (after {final_cycle} cycles): {state}")
            break

print()
print(sent_pulses)
print(sent_pulses[LOW] * sent_pulses[HIGH])
print()



# If a cycle was detected
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

print(f"Total LOW pulses after {final_cycle} cycles: {total_sent_pulses[LOW]}")
print(f"Total HIGH pulses after {final_cycle} cycles: {total_sent_pulses[HIGH]}")
print(f"Product of LOW and HIGH pulses: {total_sent_pulses[LOW] * total_sent_pulses[HIGH]}")



# 814934624
