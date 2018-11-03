#!/usr/bin/env python3

import unittest
from collections import namedtuple

def find_largest(banks):
    largest = banks[0]
    largest_index = 0
    for i in range(1, len(banks)):
        if banks[i] > largest:
            largest = banks[i]
            largest_index = i
    return largest_index

def distribute(index, banks):
    value = banks[index]
    banks[index] = 0
    i = (index + 1) % len(banks)
    while value > 0:
        banks[i] = banks[i] + 1
        value = value - 1
        i = (i + 1) % len(banks)

def calc_steps(banks):
    found = {}
    steps = 0
    while found.get(hash(tuple(banks))) is None:
        found[hash(tuple(banks))] = steps
        largest = find_largest(banks)
        distribute(largest, banks)
        steps = steps + 1
    cycles_in_loop = steps - found[hash(tuple(banks))]
    return (steps, cycles_in_loop)

class TestThis(unittest.TestCase):
    def test_largest(self):
        self.assertEqual(find_largest([4, 5, 5, 1]), 1)
    def test_calc_steps(self):
        self.assertEqual(calc_steps([0, 2, 7, 0]), (5, 4))

if __name__ == "__main__":
    #unittest.main()
    with open("input6.txt", "r") as f:
        data = f.read()
        banks = [int(d) for d in data.strip().split()]
        print("Banks before: {}", banks)
        print("Number of banks: {}", len(banks))
        (steps, cycles_in_loop) = calc_steps(banks)
        print("Banks after: {}", banks)
        print("Number of steps to reach loop (problem 1): {}", steps)
        print("Number of step in loop (problem 2): {}", cycles_in_loop)
