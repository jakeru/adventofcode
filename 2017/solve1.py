#!/usr/bin/env python3

import unittest

def calculate_sum(digits, offset):
    sum = 0
    for i in range(0, len(digits)):
        other = (i + offset) % len(digits)
        if digits[i] == digits[other]:
            sum += int(digits[i])
    return sum

def calculate_sum1(digits):
    return calculate_sum(digits, 1)

def calculate_sum2(digits):
    if len(digits) % 2 != 0:
        raise ValueError("Number of digits must be even")
    return calculate_sum(digits, len(digits) // 2)

class TestSum(unittest.TestCase):
    def test1(self):
        self.assertEqual(calculate_sum1("1122"), 3)
        self.assertEqual(calculate_sum1("1111"), 4)
        self.assertEqual(calculate_sum1("1234"), 0)
        self.assertEqual(calculate_sum1("91212129"), 9)
        self.assertEqual(calculate_sum1("00"), 0)
        self.assertEqual(calculate_sum1("1212"), 0)
        self.assertEqual(calculate_sum1("99"), 18)
    def test2(self):
        self.assertEqual(calculate_sum2("1212"), 6)
        self.assertEqual(calculate_sum2("1221"), 0)
        self.assertEqual(calculate_sum2("123425"), 4)
        self.assertEqual(calculate_sum2("123123"), 12)
        self.assertEqual(calculate_sum2("12131415"), 4)

if __name__ == "__main__":
    with open("input1.txt", "r") as f:
        digits = f.read().strip()
        print("Digits: %u" % len(digits))
        print("Sum1: %u" % calculate_sum1(digits))
        print("Sum2: %u" % calculate_sum2(digits))
    unittest.main()
