#!/usr/bin/env python3

import unittest
from collections import namedtuple

Instruction = namedtuple("Instruction", "reg op val cond_reg cond_op cond_val")

class Machine:
    def __init__(self):
        self.regs = {}
        self.highest_value_held = None
    @staticmethod
    def parse(line):
        # Parse a line like this:
        # b inc 5 if a < 4
        p = line.split()
        if len(p) != 7:
            raise(ValueError("Bad line: '{}', not expected number of tokens".format(line)))
        if p[3] != "if":
            raise(ValueError("Bad line: '{}', missing if".format(line)))
        return Instruction(p[0], p[1], int(p[2]), p[4], p[5], int(p[6]))
    def eval_cond(self, instr):
        if not instr.cond_reg in self.regs:
            self.regs[instr.cond_reg] = 0
        lv = self.regs[instr.cond_reg]
        rv = instr.cond_val
        if instr.cond_op == "<":
            return lv < rv
        elif instr.cond_op == "<=":
            return lv <= rv
        elif instr.cond_op == "==":
            return lv == rv
        elif instr.cond_op == "!=":
            return lv != rv
        elif instr.cond_op == ">=":
            return lv >= rv
        elif instr.cond_op == ">":
            return lv > rv
        else:
            raise(ValueError("Unknown condition operator: {}".format(instr.cond_op)))
    def eval(self, instr):
        if not instr.reg in self.regs:
            self.regs[instr.reg] = 0
        if not self.eval_cond(instr):
            return
        if instr.op == "inc":
            self.regs[instr.reg] = self.regs[instr.reg] + instr.val
        elif instr.op == "dec":
            self.regs[instr.reg] = self.regs[instr.reg] - instr.val
        else:
            raise(ValueError("Unknown operator: {}".format(instr.op)))
        if self.highest_value_held is None or self.highest_value_held < self.regs[instr.reg]:
            self.highest_value_held = self.regs[instr.reg]
    def find_largest_reg(self):
        reg = None
        for k,v in self.regs.items():
            if reg is None or v > self.regs[reg]:
                reg = k
        return reg

class TestThis(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(Machine.parse("b inc 5 if a < 4"), Instruction("b", "inc", 5, "a", "<", 4))
    def test_eval(self):
        m = Machine()
        m.eval(m.parse("b inc 5 if a > 1"))
        self.assertEqual(m.regs["b"], 0)
        m.eval(m.parse("a inc 1 if b < 5"))
        self.assertEqual(m.regs["a"], 1)
        m.eval(m.parse("c dec -10 if a >= 1"))
        self.assertEqual(m.regs["c"], 10)
        m.eval(m.parse("c inc -20 if c == 10"))
        self.assertEqual(m.regs["c"], -10)
        self.assertEqual(m.find_largest_reg(), "a")
        self.assertEqual(m.regs[m.find_largest_reg()], 1)

if __name__ == "__main__":
    #unittest.main()
    with open("input8.txt", "r") as f:
        m = Machine()
        lines = f.readlines()
        for line in lines:
            m.eval(m.parse(line))
        largest_reg = m.find_largest_reg()
        print("Largest reg is {} which has the value {}".format(largest_reg, m.regs[largest_reg]))
        print("Highest value held: {}".format(m.highest_value_held))
