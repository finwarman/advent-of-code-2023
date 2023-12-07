#! /usr/bin/env python3
import numpy as np

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.strip().split(' ') for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

FIVE_OF_A_KIND  = 100
FOUR_OF_A_KIND  = 90
FULL_HOUSE      = 80
THREE_OF_A_KIND = 70
TWO_PAIR        = 60
ONE_PAIR        = 50
HIGH_CARD       = 40

CARD_VALUES = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'][::-1]

def hand_strength(hand):
    assert(len(hand) == 5)
    _, counts = np.unique(hand, return_counts=True)
    unique_elements_count = len(set(hand))
    if unique_elements_count == 1:
        return FIVE_OF_A_KIND
    if unique_elements_count == 2:
        if hand.count(hand[0]) in [1, 4]:
            return FOUR_OF_A_KIND
        return FULL_HOUSE
    if unique_elements_count == 3:
        if 1 in counts and 3 in counts:
            return THREE_OF_A_KIND
        return TWO_PAIR
    if unique_elements_count == 4:
        if 2 in counts:
            return ONE_PAIR
    return HIGH_CARD

def get_strongest(hand, index=0, max_strength=float('-inf'), candidates=None):
    assert len(hand) == 5

    # each 'J' can be any other card in the hand (including 'J')
    if candidates is None:
        candidates = list(set(hand))

    # there are no more replacements in this recursion, hand evaluate strength
    if index >= len(hand):
        current_value = hand_strength(hand)
        return max(max_strength, current_value)

    # recursively produce all possible hands for _this_ J
    if hand[index] == 'J':
        for value in candidates:
            new_hand = hand[:index] + [value] + hand[index+1:]
            max_strength = get_strongest(new_hand, index + 1, max_strength, candidates)
    else:
        max_strength = get_strongest(hand, index + 1, max_strength, candidates)

    return max_strength

def hand_sort(hand):
    _, _, strength, card_values = hand
    return tuple([strength] + card_values)

parsed_hands = []
for hand, bid in rows:
    hand, bid = list(hand), int(bid)
    strength = get_strongest(hand)
    card_values = [CARD_VALUES.index(c) for c in hand]
    parsed_hands.append((hand, bid, strength, card_values))

sorted_hands = sorted(parsed_hands, key=hand_sort)

total = 0
for rank, hand in enumerate(sorted_hands):
    _, bid, strength, _ = hand
    total += (rank+1) * bid

print(total)

# 243101568
