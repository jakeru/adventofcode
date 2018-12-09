#!/usr/bin/env python3

# By Jakob Ruhe 2018-12-08

import unittest
import collections
import re
from functools import reduce

class Node:
    def __init__(self):
        self.children = []
        self.metadata = []
    def metadata_sum_this(self):
        return reduce(lambda sum, m: sum + m, self.metadata, 0)
    def metadata_sum_children(self):
        return reduce(lambda sum, c: sum + c.metadata_sum(), self.children, 0)
    def metadata_sum(self):
        return self.metadata_sum_this() + self.metadata_sum_children()
    def value(self):
        if self.children:
            indexes = filter(lambda i: i > 0 and i <= len(self.children), self.metadata)
            return reduce(lambda sum, i: sum + self.children[i - 1].value(), indexes, 0)
        else:
            return self.metadata_sum_this()

def string_as_ints(str):
    return [int(s) for s in str.split()]

def build_tree(ints):
    num_children = next(ints)
    metadata_size = next(ints)
    node = Node()
    for c in range(num_children):
        node.children.append(build_tree(ints))
    for m in range(metadata_size):
        node.metadata.append(next(ints))
    return node

class TestThis(unittest.TestCase):
    def test_string_as_ints(self):
        self.assertEqual(string_as_ints("  1 2\n 33    44  "), [1, 2, 33, 44])
    def test_sum(self):
        int_list = string_as_ints("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2")
        root = build_tree(iter(int_list))
        self.assertEqual(root.metadata_sum(), 138)
    def test_value(self):
        int_list = string_as_ints("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2")
        root = build_tree(iter(int_list))
        self.assertEqual(root.value(), 66)

if __name__ == "__main__":
    #unittest.main()
    with open("p8_input.txt") as f:
        data = f.read()
    int_list = string_as_ints(data)
    root = build_tree(iter(int_list))
    print("Answer to subproblem 1 is: {}".format(root.metadata_sum()))
    print("Answer to subproblem 2 is: {}".format(root.value()))
