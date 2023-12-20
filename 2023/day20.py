#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-20

from abc import abstractmethod
import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils


def parse_input(input):
    return input.strip().split("\n")


class Mod:
    @abstractmethod
    def handle_input_from(self, name, value):
        pass

    def add_input(self, name):
        pass

    @abstractmethod
    def get_state(self):
        pass

    @staticmethod
    def module_from_prefix(prefix):
        if prefix == "%":
            return FlipFlop()
        elif prefix == "&":
            return Conjunction()
        elif prefix == "":
            return Broadcaster()
        else:
            raise ValueError(prefix)


class Broadcaster(Mod):
    def handle_input_from(self, name, value):
        assert not value
        return True

    def get_state(self):
        return False


class FlipFlop(Mod):
    """
    Flip-flop (prefix%):
    Init: Low
    Signal: High -> Nothing happens
    Signal Low -> Flips state
    """

    def __init__(self):
        self._state = False

    def handle_input_from(self, name, value):
        if value:
            return False
        self._state = not self._state
        return True

    def get_state(self):
        return self._state


class Conjunction(Mod):
    """
    Conjunction (prefix &):
    Remembers most recent pulse received from each of the
    connected modules.
    Init: All signals are low
    Signal: Low if all inputs are high, otherwise high
    Sounds like a NAND gate.
    """

    def __init__(self):
        # self._inputs = defaultdict(bool)
        # self._inputs = {k:False for k in inputs}
        self._inputs = {}

    def add_input(self, name):
        self._inputs[name] = False

    def handle_input_from(self, name, value):
        self._inputs[name] = value
        return True

    def get_state(self):
        return not all(self._inputs.values())


class Output(Mod):
    def handle_input_from(self, name, value):
        return False

    def get_state(self):
        raise NotImplementedError


def press_button(modules, sent_pulses):
    active_pulses = []
    active_pulses.append(("button", False, "broadcaster"))
    while active_pulses:
        source, value, dest = active_pulses.pop(0)
        print(f"{source} -{'high' if value else 'low'}-> {dest}")
        sent_pulses.append(value)
        mod = modules[dest]
        if mod[0].handle_input_from(source, value):
            outgoing_value = mod[0].get_state()
            for d in mod[1]:
                active_pulses.append((dest, outgoing_value, d))


def solve1(entries):
    modules = {}
    for line in entries:
        m = re.match(r"([%&]?)([a-z]+) -> (.+)", line)
        assert m
        mod_type = Mod.module_from_prefix(m[1])
        modules[m[2]] = (mod_type, tuple(m[3].split(", ")))

    output_modules = {}
    for k, v in modules.items():
        for d in v[1]:
            if d not in modules:
                output_modules[d] = (Output(), ())

    for k, v in output_modules.items():
        modules[k] = v

    for k, v in modules.items():
        destinations = v[1]
        for dest in destinations:
            modules[dest][0].add_input(k)

    for k, v in modules.items():
        print(f"{k}: {v}")

    sent_pulses = []

    for _ in range(1000):
        press_button(modules, sent_pulses)

    num_on = sum(1 for p in sent_pulses if p)
    num_off = sum(1 for p in sent_pulses if not p)
    print(f"num_on {num_on}")
    print(f"num_off {num_off}")

    return num_on * num_off


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input1 = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

    input2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input1)), 32000000)
        self.assertEqual(solve1(parse_input(self.input2)), 11687500)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input1)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
