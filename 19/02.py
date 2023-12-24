#! /usr/bin/env python3

from collections import defaultdict
from math import prod

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

workflows = [row.strip() for row in data.split('\n\n')[0].split('\n')]

# ==== SOLUTION ====

workflow_mappings = defaultdict(list)
for workflow in workflows:
    name, rules_str = workflow[:-1].split('{')
    rules = rules_str.split(',')

    # conditional jumps
    for rule_str in rules[:-1]:
        if ':' in rule_str:
            condition, dest = rule_str.split(':')
            rating_key, comp_op, value = condition[0], condition[1], int(condition[2:])
            workflow_mappings[name].append((rating_key, comp_op, value, dest))

    # final step - use dummy condition
    workflow_mappings[name].append(('x', '>', 0, rules[-1]))

RATING_KEYS   = ('x', 'm', 'a', 's')
DEFAULT_RANGE = (1, 4001)

# convert each condition in 'rules' to its literal false equivalent
# e.g. ('>', value) -> ('<', value-1)  e.g. x>10 -> x<11
#      ('<', value) -> ('>', value+1)  e.g. x<10 -> x>9
def get_false_conditions(rules):
    false_conditions = []
    for e in rules:
        e_rating_key, e_operator, e_value = e[0], e[1], int(e[2])
        false_condition = ( # e.g. ('x', '>', 10)
            e_rating_key,
            ('<' if e_operator == '>' else '>'),
            e_value + (1 if e_operator == '>' else -1),
        )
        false_conditions.append(false_condition)
    return false_conditions

# determine all valid ranges to 'accept' paths, backwards from 'A' -> 'in'
def get_accepted_condition_paths(workflow_mappings):
    # bfs queue: [(current_workflow, conditions),]
    queue = [("A", [])]
    valid_paths = []

    while queue:
        curr_workflow, conditions = queue.pop(0)
        # end of current path, store conditions for path
        if curr_workflow == "in":
            valid_paths.append(conditions)
            continue

        for name, rule in workflow_mappings.items():
            for i, test in enumerate(rule):
                rating_key, comp_op, value, dest = test

                # conditions with dest of current workflow only
                if dest != curr_workflow:
                    continue

                curr_condition = (rating_key, comp_op, value)

                # get negations of conditions up to current rule
                # (x>10 -> x<11, etc.)
                false_conditions = get_false_conditions(rule[:i])

                new_conditions = conditions + false_conditions + [curr_condition]
                queue.append((name, new_conditions))

    return valid_paths

# apply conditions in code paths to determine the number of valid combinations
def count_path_valid_combinations(valid_paths):
    ans = 0
    for conditions in valid_paths:
        valid_ranges = {rating: list(DEFAULT_RANGE) for rating in RATING_KEYS}
        for cond in conditions:
            category, operator, v = cond

            if operator == ">":
                valid_ranges[category][0] = max(valid_ranges[category][0], v+1)
            else: # "<"
                valid_ranges[category][1] = min(valid_ranges[category][1], v)

        ans += prod([r[1] - r[0] for r in valid_ranges.values()])

    return ans

# calculate the number of accepted combinations for the provided workflows
valid_paths = get_accepted_condition_paths(workflow_mappings)
accepted_combingations = count_path_valid_combinations(valid_paths)

print(accepted_combingations)

# 125317461667458
