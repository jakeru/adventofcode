#!/usr/bin/env python3

import unittest

def get_puzzle_input():
    with open("p2_input.txt", "r") as f:
        return f.readlines()

def count_letters(str):
    count = {}
    for c in str:
        if c in count:
            count[c] = count[c] + 1
        else:
            count[c] = 1
    return count

def has_num(count, num):
    for n in count.values():
        if n == num:
            return True
    return False

class TestThis(unittest.TestCase):
    def test_count_letters(self):
        self.assertFalse(has_num(count_letters("abcdef"), 2))
        self.assertFalse(has_num(count_letters("abcdef"), 3))
        self.assertTrue(has_num(count_letters("bababc"), 2))
        self.assertTrue(has_num(count_letters("bababc"), 3))
        self.assertTrue(has_num(count_letters("abbcde"), 2))
        self.assertFalse(has_num(count_letters("abbcde"), 3))
        self.assertFalse(has_num(count_letters("abcccd"), 2))
        self.assertTrue(has_num(count_letters("abcccd"), 3))
        self.assertTrue(has_num(count_letters("aabcdd"), 2))
        self.assertFalse(has_num(count_letters("aabcdd"), 3))
        self.assertTrue(has_num(count_letters("abcdee"), 2))
        self.assertFalse(has_num(count_letters("abcdee"), 3))
        self.assertFalse(has_num(count_letters("ababab"), 2))
        self.assertTrue(has_num(count_letters("ababab"), 3))

if __name__ == "__main__":
    #unittest.main()
    lines = get_puzzle_input()
    num_2s = 0
    num_3s = 0
    for line in lines:
        count = count_letters(line)
        if 2 in count.values():
            num_2s = num_2s + 1
        if 3 in count.values():
            num_3s = num_3s + 1
    print("Num 2s: {}, num 3s: {}, checksum: {}".format(num_2s, num_3s, num_2s * num_3s))
