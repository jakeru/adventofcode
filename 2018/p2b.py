#!/usr/bin/env python3

import unittest

def get_puzzle_input():
    with open("p2_input.txt", "r") as f:
        return f.readlines()

def diff(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Not same length: '{}' '{}'".format(s1, s2))
    num = 0
    for i in range(0, len(s1)):
        if s1[i] != s2[i]:
            num = num + 1
    return num

def first_diff(s1, s2):
    for i in range(0, len(s1)):
        if s1[i] != s2[i]:
            return i
    return None

class TestThis(unittest.TestCase):
    def test_diff(self):
        self.assertEqual(diff("abc", "abc"), 0)
        self.assertEqual(diff("abc", "abd"), 1)
        self.assertEqual(diff("abc", "aee"), 2)
        self.assertEqual(diff("abc", "fff"), 3)

if __name__ == "__main__":
    # unittest.main()
    lines = list(map(lambda line: line.strip(), get_puzzle_input()))
    for i in range(0, len(lines)):
        for j in range(i + 1, len(lines)):
            if diff(lines[i], lines[j]) != 1:
                continue
            p = first_diff(lines[i], lines[j])
            common = lines[i][:p] + lines[i][(p+1):]
            print("Found {} at {} and {} at {}, common: {}".format(lines[i], i, lines[j], j, common))
