#!/usr/bin/env python3

# By Jakob Ruhe 2018-12-03

import unittest
import collections
import re

Claim = collections.namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])

def get_puzzle_input():
    with open("p3_input.txt", "r") as f:
        return f.readlines()

def claim_from_str(str):
    m = re.search(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", str)
    params = [int(m.group(i)) for i in range(1,6)]
    return Claim(*params)

def coord_from_xy(x, y):
    return "x:{},y:{}".format(x, y)

def apply_claim(cells, claim):
    for y in range(claim.height):
        for x in range(claim.width):
            c = coord_from_xy(x + claim.left, y + claim.top)
            if c in cells:
                cells[c] = cells[c] + 1
            else:
                cells[c] = 1

def is_claim_intact(cells, claim):
    for y in range(claim.height):
        for x in range(claim.width):
            c = coord_from_xy(x + claim.left, y + claim.top)
            if cells[c] != 1:
                return False
    return True

class TestThis(unittest.TestCase):
    def test_claim_from_str(self):
        self.assertEqual(claim_from_str("#123 @ 456,789: 1122x3344"), Claim(123, 456, 789, 1122, 3344))

if __name__ == "__main__":
    #unittest.main()
    lines = get_puzzle_input()
    cells = {}
    claims = list(map(lambda line: claim_from_str(line), lines))
    for claim in claims:
        apply_claim(cells, claim)
    collisions = len(list(filter(lambda v: v > 1, cells.values())))
    print("Square inches of collisions: {}".format(collisions))
    for claim in claims:
        if is_claim_intact(cells, claim):
            print("Intact claim: {}".format(claim.id))
