#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils
from functools import cmp_to_key

def parse_input(input):
    return input.strip().split("\n")

# 0 nothing
# 1 one pair
# 2 two of a kind
# 3 three of a kind
# 4 full house
# 5 four of a kind
# 6 five of a kind

def card_value(c):
    cards = "23456789TJQKA"
    return cards.index(c) + 2

def type_of_hand(hand):
    count = defaultdict(int)
    for h in hand:
        count[h] += 1
    if 5 in count.values():
        return 6
    elif 4 in count.values():
        return 5
    elif 3 in count.values() and 2 in count.values():
        return 4
    elif 3 in count.values():
        return 3
    elif len([c for c in count.values() if c == 2]) == 2:
        return 2
    elif 2 in count.values():
        return 1
    else:
        return 0


def compare(bh1, bh2):
    h1 = bh1[0]
    h2 = bh2[0]
    t1 = type_of_hand(h1)
    t2 = type_of_hand(h2)
    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    for c1, c2 in zip(h1, h2):
        if card_value(c1) < card_value(c2):
            return -1
        elif card_value(c1) > card_value(c2):
            return 1
    raise ValueError()



def solve1(entries):
    card_bets = []
    for line in entries:
        c, b = line.split()
        card_bets.append((c, int(b)))
    print(card_bets)
    sorted_card_bets = sorted(card_bets, key=cmp_to_key(compare))
    print(sorted_card_bets)
    total = 0
    for i, hand_bet in enumerate(sorted_card_bets):
        rank = i + 1
        total += (i + 1) * hand_bet[1]
    return total


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 6440)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
