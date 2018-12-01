#!/usr/bin/env python3

from p1 import *

if __name__ == "__main__":
    value = 0
    values = {}
    values[value] = True
    first_value_seen_twice = None
    changes = get_changes_from_file()
    iterations = 0
    while first_value_seen_twice is None:
        for c in changes:
            iterations = iterations + 1
            value = value + c
            if value in values:
                first_value_seen_twice = value
                break
            values[value] = True
    print("First value seen twice: {} after {} iterations".format(first_value_seen_twice, iterations))
