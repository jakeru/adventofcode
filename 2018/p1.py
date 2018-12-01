#!/usr/bin/env python3

import re

def get_changes_from_file():
    changes = []
    with open("p1_input.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            m = re.search(r"([+-])(\d+)", line)
            op = m.group(1)
            v = int(m.group(2))
            if op == '+':
                changes.append(v)
            elif op == '-':
                changes.append(-v)
            else:
                raise ValueError("Expected + or -, got: {}".format(op))
    return changes
