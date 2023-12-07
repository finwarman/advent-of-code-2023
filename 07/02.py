#! /usr/bin/env python3
import numpy as np
from collections import Counter

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

CARD_VALUES = {
    card: i for i, card in enumerate(
    ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'][::-1])
}

def hand_strength(hand):
    uniq, counts = np.unique(hand, return_counts=True)
    unique_count = len(uniq)
    if unique_count == 1:
        return FIVE_OF_A_KIND
    if unique_count == 2:
        if hand.count(hand[0]) in [1, 4]:
            return FOUR_OF_A_KIND
        return FULL_HOUSE
    if unique_count == 3:
        if 1 in counts and 3 in counts:
            return THREE_OF_A_KIND
        return TWO_PAIR
    if unique_count == 4:
        if 2 in counts:
            return ONE_PAIR
    return HIGH_CARD


def get_strongest(hand):
    if 'J' in hand:
        uniq_cards, counts = np.unique(hand, return_counts=True)
        if 5 in counts: return FIVE_OF_A_KIND

        # replace 'J' with the most frequent, maximum value card
        candidates = [(card, count) for card, count in zip(uniq_cards, counts) if card != 'J']
        best_card = max(candidates, key=lambda entry: (entry[1], CARD_VALUES[entry[0]]))[0]
        hand = [best_card if card == 'J' else card for card in hand]

    return hand_strength(hand)


def hand_sort(hand):
    _, _, strength, card_values = hand
    return tuple([strength] + card_values)


parsed_hands = []
for hand, bid in rows:
    hand, bid = list(hand), int(bid)
    strength = get_strongest(hand)
    card_values = [CARD_VALUES[c] for c in hand]
    parsed_hands.append((hand, bid, strength, card_values))

sorted_hands = sorted(parsed_hands, key=hand_sort)

total = 0
for rank, hand in enumerate(sorted_hands):
    _, bid, strength, _ = hand
    total += (rank+1) * bid

print(total)

# 243101568
