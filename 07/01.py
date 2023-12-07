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

CARD_VALUES = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'][::-1]

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

def hand_sort(hand):
    _, _, strength, card_values = hand
    return tuple([strength] + card_values)

parsed_hands = []
for hand, bid in rows:
    hand, bid = list(hand), int(bid)
    strength = hand_strength(hand)
    card_values = [CARD_VALUES.index(c) for c in hand]
    parsed_hands.append((hand, bid, strength, card_values))

sorted_hands = sorted(parsed_hands, key=hand_sort)

total = 0
for rank, hand in enumerate(sorted_hands):
    _, bid, strength, _ = hand
    total += (rank+1) * bid

print(total)

# 241344943
