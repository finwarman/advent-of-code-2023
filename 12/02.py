#! /usr/bin/env python3

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip().split(' ') for row in data.split('\n')[:-1]]

springs     = [row[0] for row in rows]
group_sizes = [tuple(int(x) for x in row[1].split(',')) for row in rows]

# ==== SOLUTION ====

MULTIPLIER = 5

OPERATIONAL, DAMAGED, UNKNOWN = ('.', '#', '?')

ARRANGEMENT_CACHE = {}

def get_valid_arrangements(springs, groups):
    key = f"{springs}{groups}"

    # cache calls to this function
    if key in ARRANGEMENT_CACHE:
        return ARRANGEMENT_CACHE[key]

    # there are more groups to process, but no space for them
    if groups and not springs:
        return 0

    # all groups are done, check if result is valid
    if not groups:
        if DAMAGED in springs:
            return 0
        return 1

    curr_char, curr_group_size = springs[0], groups[0]

    def currentCharOperational():
        # try the next spring, for the current group
        return get_valid_arrangements(springs[1:], groups)

    def currentCharDamaged():
        # if current spring is damaged, then the rest of this group must
        # be damaged and contiguous from the current spring

        # there must be enough springs left to fill the group size
        if len(springs) < curr_group_size:
            return 0
        # they must all be either 'damaged' or 'unknown'
        if OPERATIONAL in springs[:curr_group_size]:
            return 0

        # current group is valid - we are done if this is the last gruop
        if len(springs) == curr_group_size:
            if len(groups) == 1:
                return 1
            # else, we can't fit any more groups
            return 0

        # the spring after a full group cannot be damaged, since groups
        # are noncontiguous
        if springs[curr_group_size] == DAMAGED:
            return 0

        # move on to next group, skipping to first character after this group
        return get_valid_arrangements(springs[curr_group_size+1:], groups[1:])

    def currentCharUnknown():
        # recurse through both paths from this point
        return currentCharDamaged() + currentCharOperational()

    next_char_operations = {
        UNKNOWN:     currentCharUnknown,
        DAMAGED:     currentCharDamaged,
        OPERATIONAL: currentCharOperational,
    }

    # recursively determine count of valid arrangements
    total = next_char_operations[curr_char]()
    ARRANGEMENT_CACHE[key] = total

    return total

# extend by repeat factor
springs      = [((row+'?') * MULTIPLIER)[:-1] for row in springs]
group_sizes  = [row * MULTIPLIER for row in group_sizes]

total = sum(
    get_valid_arrangements(springs, groups)
    for springs, groups in zip(springs, group_sizes)
)

print(total)

# 17391848518844
