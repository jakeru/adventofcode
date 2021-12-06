#!/usr/bin/env python3

# By Jakob Ruhe 2021-12-04

# Note: This is not cleaned up after the problem got solved.

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils

def parse_input(input):
    return input.strip().split("\n")

class Board:
    def __init__(self, squares):
        self.squares = squares
        self.marked = set()

    def check_row(self, y):
        for x in range(5):
            if (x, y) not in self.marked:
                return False
        return True

    def check_col(self, x):
        for y in range(5):
            if (x, y) not in self.marked:
                return False
        return True

    def is_winner(self):
        for y in range(5):
            if self.check_row(y):
                return True
        for x in range(5):
            if self.check_col(x):
                return True
        return False

    def draw(self, number):
        num = 0
        for y in range(5):
            for x in range(5):
                if self.squares[y][x] == number:
                    num += 1
                    self.marked.add((x,y))
        return num

    def sum_of_unmarked(self):
        unmarked = 0
        for y in range(5):
            for x in range(5):
                if (x, y) not in self.marked:
                    unmarked += self.squares[y][x]
        print("unmarked", unmarked)
        return unmarked


def get_winning_board(numbers, boards):
    for i in range(len(numbers)):
        drawn = numbers[0:i+1]
        current = numbers[i]
        print("At ", i, "drawn", drawn, "current", current)
        for b in boards:
            if b.draw(current) > 0 and b.is_winner():
                return current, b
    return None

def get_loosing_board(numbers, boards):
    unfinished_boards = set(boards)
    for i in range(len(numbers)):
        drawn = numbers[0:i+1]
        current = numbers[i]
        print("At ", i, "drawn", drawn, "current", current)
        for b in boards:
            if b not in unfinished_boards:
                continue
            if b.draw(current) > 0 and b.is_winner():
                unfinished_boards.remove(b)
                if len(unfinished_boards) == 0:
                    return current, b
    return None

def solve1(entries):
    numbers = list(map(int, entries[0].split(",")))
    boards = []
    print("numbers", numbers)
    for b in range(2, len(entries), 6):
        print("b", b)
        squares = []
        for y in range(5):
            squares.append(list(map(int, entries[b+y].strip().split())))
        boards.append(Board(squares))
        print("board", "b", squares)
    last_drawn, board = get_winning_board(numbers, boards)
    return last_drawn * board.sum_of_unmarked()

def solve2(entries):
    numbers = list(map(int, entries[0].split(",")))
    boards = []
    print("numbers", numbers)
    for b in range(2, len(entries), 6):
        print("b", b)
        squares = []
        for y in range(5):
            squares.append(list(map(int, entries[b+y].strip().split())))
        boards.append(Board(squares))
        print("board", "b", squares)
    last_drawn, board = get_loosing_board(numbers, boards)
    return last_drawn * board.sum_of_unmarked()

# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""
    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 4512)
    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 1924)

if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
