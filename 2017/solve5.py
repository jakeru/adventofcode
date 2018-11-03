#!/usr/bin/env python3

import unittest
from collections import namedtuple

def calc_steps1(instructions):
    steps = 0
    pos = 0
    while pos < len(instructions):
        next = pos + instructions[pos]
        instructions[pos] = instructions[pos] + 1
        pos = next
        steps = steps + 1
    return steps

def calc_steps2(instructions):
    steps = 0
    pos = 0
    while pos < len(instructions):
        next = pos + instructions[pos]
        if instructions[pos] >= 3:
            instructions[pos] = instructions[pos] - 1
        else:
            instructions[pos] = instructions[pos] + 1
        pos = next
        steps = steps + 1
    return steps

class TestThis(unittest.TestCase):
    def test1(self):
        instructions = [0, 3, 0, 1, -3]
        self.assertEqual(calc_steps1(instructions), 5)
        self.assertEqual(instructions, [2,  5,  0,  1, -2])
    def test2(self):
        instructions = [0, 3, 0, 1, -3]
        self.assertEqual(calc_steps2(instructions), 10)
        self.assertEqual(instructions, [2, 3, 2, 3, -1])

if __name__ == "__main__":
    #unittest.main()
    with open("input5.txt", "r") as f:
        lines = f.readlines()
        instructions = [int(line) for line in lines]
        print("Instructions: {}", len(instructions))
        i1 = list(instructions)
        steps1 = calc_steps1(i1)
        print("Steps 1: {}", steps1)
        i2 = list(instructions)
        steps2 = calc_steps2(i2)
        print("Steps 2: {}", steps2)
