#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-15

import os
import unittest


def parse_input(input):
    return input.strip().split("\n")


def calc_hash(string):
    h = 0
    for c in string:
        h += ord(c)
        h *= 17
        h = h % 256
    return h


def solve1(entries):
    total = 0
    for line in entries:
        tokens = line.split(",")
        for t in tokens:
            h = calc_hash(t)
            print(f"hash of '{t}' is {h}")
            total += h
    return total


def focus_power(boxes):
    total = 0
    for box_num, box in boxes.items():
        for pos, lens in enumerate(box):
            fp = (box_num + 1) * (pos + 1) * lens[1]
            total += fp
    return total


def find_label_in_box(label, box):
    for i, tok in enumerate(box):
        if label == tok[0]:
            return i
    return None


def solve2(entries):
    tokens = []
    for line in entries:
        tokens.extend(line.split(","))
    boxes = {}
    for t in tokens:
        c = "=" if "=" in t else "-"
        label, focal_length = t.split(c)
        h = calc_hash(label)
        if h not in boxes:
            boxes[h] = []
        if c == "=":
            pos = find_label_in_box(label, boxes[h])
            if pos is not None:
                boxes[h][pos] = (label, int(focal_length))
            else:
                boxes[h].append((label, int(focal_length)))
        else:
            pos = find_label_in_box(label, boxes[h])
            if pos is not None:
                boxes[h].pop(pos)

    return focus_power(boxes)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 1320)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 145)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
