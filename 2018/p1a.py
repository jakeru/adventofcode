#!/usr/bin/env python3

from p1 import *

if __name__ == "__main__":
    value = 0
    changes = get_changes_from_file()
    for c in changes:
        value = value + c
    print("Value: {}".format(value))
