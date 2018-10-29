#!/usr/bin/env python3

import unittest

def str_to_cells(str):
    cells = []
    lines = str.strip().split("\n")
    for line in lines:
        words = line.split()
        numbers = []
        for w in words:
            numbers.append(int(w))
        cells.append(numbers)
    return cells

def find_max(digits):
    max = digits[0]
    for d in digits:
        if d > max:
            max = d
    return max

def find_min(digits):
    min = digits[0]
    for d in digits:
        if d < min:
            min = d
    return min

def find_max_diff(digits):
    min = find_min(digits)
    max = find_max(digits)
    return max - min

def checksum1(cells):
    sum = 0
    for row in cells:
        sum += find_max_diff(row)
    return sum

def find_divs(digits):
    sum = 0
    for i in range(0, len(digits)):
        for j in range(0, len(digits)):
            if i != j and digits[j] != 0 and digits[i] % digits[j] == 0:
                sum += digits[i] // digits[j]
    return sum

def checksum2(cells):
    sum = 0
    for row in cells:
        sum += find_divs(row)
    return sum

class TestSum(unittest.TestCase):
    def test_find_min_max(self):
        self.assertEqual(find_min([99]), 99)
        self.assertEqual(find_max([99]), 99)
        self.assertEqual(find_max([1, 2, 3, 2]), 3)
        self.assertEqual(find_min([1, 2, 3, 2]), 1)
    def test1(self):
        str = """5 1 9 5
                    7 5 3
                    2 4 6 8
                    """
        cells = str_to_cells(str)
        print(cells)
        self.assertEqual(checksum1(cells), 18)
    def test_divs(self):
        self.assertEqual(find_divs([5, 9, 2, 8]), 4)
        self.assertEqual(find_divs([9, 4, 7, 3]), 3)
        self.assertEqual(find_divs([3, 8, 6, 5]), 2)
    def test2(self):
        str = "5 9 2 8\n9 4 7 3\n3 8 6 5"
        cells = str_to_cells(str)
        self.assertEqual(checksum2(cells), 9)

if __name__ == "__main__":
    with open("input2.txt", "r") as f:
        data = f.read()
        cells = str_to_cells(data)
        print("checksum1: %u" % checksum1(cells))
        print("checksum2: %u" % checksum2(cells))
    unittest.main()
