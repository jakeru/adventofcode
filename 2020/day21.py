#!/usr/bin/env python3

# By Jakob Ruhe 2020-12-21

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple

def parse_input(input):
    lines = input.strip().split("\n")
    food_list = []
    for line in lines:
        ingrediens_str, allergens_str = line.split(" (contains ")
        food_list.append((set(ingrediens_str.split()),
                          set(allergens_str.replace(")", "").split(", "))))
    return food_list

def find_allergene_not_including(foods, allergene, ingrediens):
    for f in foods:
        if ingrediens not in f[0] and allergene in f[1]:
            return f
    return None

def solve1(entries):
    print("foods")
    for f in entries:
        print(f)
    possible_allergenes = defaultdict(set)
    for e in entries:
        for i in e[0]:
            for a in e[1]:
                possible_allergenes[i].add(a)
    print("possible_allergenes")
    for i,p in possible_allergenes.items():
        print("-", i, ":", " ".join(p))
    #print("possible_allergenes", possible_allergenes)
    ingrediens_list = defaultdict(set)
    for e in entries:
        for i in e[0]:
            for a in e[1]:
                ingrediens_list[a].add(i)
    print("ingrediens_list")
    for a,i in ingrediens_list.items():
        print("-", a, ":", " ".join(i))
    table = {}
    for i,p in possible_allergenes.items():
        table[i] = [a in p for a in ingrediens_list]
    print("table")
    print("i", " ".join(ingrediens_list.keys()))
    for i,t in table.items():
        print("-", i, " ".join(map(str, t)))
    for i,p in possible_allergenes.items():
        remove = set()
        for a in p:
            f = find_allergene_not_including(entries, a, i)
            if f is not None:
                print("Removing allergene", a, "from ingrediens", i, "food", f)
                remove.add(a)
        for a in remove:
            p.remove(a)
    print("possible_allergenes after removal")
    for i,p in possible_allergenes.items():
        print("-", i, ":", " ".join(p))
    res = 0
    for f in entries:
        for a,p in possible_allergenes.items():
            res += not p and a in f[0]
    return res


def solve2(entries):
    pass

# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""
    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 5)
    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)

if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
