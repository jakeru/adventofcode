#!/usr/bin/env python3

# By Jakob Ruhe 2018-12-09

import unittest
import collections
import re
from functools import reduce

class Game:
    def __init__(self, num_players, last_marble):
        self.player_scores = [0] * num_players
        self.last_marble = last_marble
        self.circle = [0]
        self.current_marble_pos = 0
        self.current_marble = 0
    def highest_score(self):
        return max(self.player_scores)
    def circle_index(self, index):
        return index % len(self.circle)
    def current_player(self):
        return (self.current_marble - 1) % len(self.player_scores)
    def print_current_state(self):
        elements = []
        for i in range(len(self.circle)):
            if i == self.current_marble_pos:
                elements.append("({})".format(self.circle[i]))
            else:
                elements.append("{}".format(self.circle[i]))
        print("[{}] {}".format(self.current_player() + 1, " ".join(elements)))
    def next(self):
        self.current_marble += 1
        player = self.current_player()
        if self.current_marble % 23 == 0:
            self.player_scores[player] += self.current_marble
            remove_pos = self.circle_index(self.current_marble_pos - 7)
            self.player_scores[player] += self.circle[remove_pos]
            del self.circle[remove_pos]
            self.current_marble_pos = remove_pos
        else:
            pos = self.circle_index(self.current_marble_pos + 2)
            self.circle.insert(pos, self.current_marble)
            self.current_marble_pos = pos
    def play(self, print_state=False):
        while self.current_marble < self.last_marble:
            self.next()
            if print_state:
                self.print_current_state()

def solve(num_players, last_marble, print_state=False):
    game = Game(num_players, last_marble)
    game.play(print_state=print_state)
    return game.highest_score()

class TestThis(unittest.TestCase):
    def test_play(self):
        self.assertEqual(solve(9, 25, print_state=True), 32)
        self.assertEqual(solve(10, 1618), 8317)
        self.assertEqual(solve(13, 7999), 146373)
        self.assertEqual(solve(17, 1104), 2764)
        self.assertEqual(solve(21, 6111), 54718)
        self.assertEqual(solve(30, 5807), 37305)

if __name__ == "__main__":
    #unittest.main()
    result1 = solve(423, 71944)
    print("The answer to subproblem 1 is: {}".format(result1))
    print("Subproblem 2 takes too long time to run... =(")
