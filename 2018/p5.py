#!/usr/bin/env python3

# By Jakob Ruhe 2018-12-05

# Note: This implementation is terribly slow!

import unittest
import collections

def can_units_react(c1, c2):
    return c1.upper() == c2.upper() and ((c1.islower() and c2.isupper()) or (c1.isupper() and c2.islower()))

def apply_one_reaction(str):
    for i in range(len(str) - 1):
        if can_units_react(str[i], str[i+1]):
            return str[:i] + str[i+2:]
    return str

def apply_reactions(str):
    while True:
        next = apply_one_reaction(str)
        if next == str:
            return str
        str = next

def find_units(str):
    units = {}
    for c in str:
        units[c.lower()] = True
    return sorted(units.keys())

def remove_unit(str, unit):
    str = str.replace(unit.lower(), "")
    str = str.replace(unit.upper(), "")
    return str

class TestThis(unittest.TestCase):
    def test_can_react(self):
        self.assertTrue(can_units_react('A', 'a'))
        self.assertTrue(can_units_react('a', 'A'))
        self.assertFalse(can_units_react('A', 'A'))
        self.assertFalse(can_units_react('a', 'a'))
    def test_apply_one_reaction(self):
        self.assertEqual(apply_one_reaction("dabAcCaCBAcCcaDA"), "dabAaCBAcCcaDA")
        self.assertEqual(apply_one_reaction("dabAaCBAcCcaDA"), "dabCBAcCcaDA")
        self.assertEqual(apply_one_reaction("dabCBAcCcaDA"), "dabCBAcaDA")
    def test_apply_reactions(self):
        self.assertEqual(apply_reactions("dabAcCaCBAcCcaDA"), "dabCBAcaDA")
    def test_find_units(self):
        self.assertEqual(find_units("AAaBc"), ['a', 'b', 'c'])
    def test_remove_unit(self):
        self.assertEqual(remove_unit("AAaBc", 'a'), "Bc")
        self.assertEqual(remove_unit("AAaBc", 'b'), "AAac")
        self.assertEqual(remove_unit("AAaBc", 'c'), "AAaB")

if __name__ == "__main__":
    #unittest.main()
    with open("p5_input.txt", "r") as f:
        str = f.read().strip()
    print("Input length: {}".format(len(str)))
    # Problem 1
    result = apply_reactions(str)
    print("Result length: {}".format(len(result)))
    # Problem 2
    units = find_units(str)
    print("Number of units: {}".format(len(units)))
    best_result = None
    best_unit = None
    for unit in units:
        out = remove_unit(str, unit)
        print("Length of str with unit {} removed: {}".format(unit, len(out)))
        result = apply_reactions(out)
        print("Output length when unit {} was removed: {}".format(unit, len(result)))
        if best_result is None or len(result) < best_result:
            best_result = len(result)
            best_unit = unit
    print("Best result is reached by removing unit {}: {}".format(best_unit, best_result))
