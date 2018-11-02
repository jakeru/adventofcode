#!/usr/bin/env python3

import unittest
from collections import namedtuple

def is_valid_passphrase1(str):
    words = str.strip().split()
    words.sort()
    last = None
    for word in words:
        if word == last:
            return False
        last = word
    return True

def is_valid_passphrase2(str):
    words = str.strip().split()
    sorted_words = []
    for w in words:
        sorted_words.append(sorted(w))
    sorted_words.sort()
    last = None
    for word in sorted_words:
        if sorted(word) == last:
            return False
        last = sorted(word)
    return True


class TestThis(unittest.TestCase):
    def test1(self):
        self.assertTrue(is_valid_passphrase1("aa bb cc dd ee"))
        self.assertFalse(is_valid_passphrase1("aa bb cc dd aa"))
        self.assertTrue(is_valid_passphrase1("aa bb cc dd aaa"))
    def test2(self):
        self.assertTrue(is_valid_passphrase2("abcde fghij"))
        self.assertFalse(is_valid_passphrase2("abcde xyz ecdab"))
        self.assertTrue(is_valid_passphrase2("a ab abc abd abf abj"))
        self.assertTrue(is_valid_passphrase2("iiii oiii ooii oooi oooo"))
        self.assertFalse(is_valid_passphrase2("oiii ioii iioi iiio"))

if __name__ == "__main__":
    #unittest.main()
    num_total = 0
    num_valid1 = 0
    num_valid2 = 0
    with open("input4.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if is_valid_passphrase1(line):
                num_valid1 = num_valid1 + 1
            if is_valid_passphrase2(line):
                num_valid2 = num_valid2 + 1
            num_total = num_total + 1
    print("Num total: {}".format(num_total))
    print("Num valid1: {}".format(num_valid1))
    print("Num valid2: {}".format(num_valid2))
