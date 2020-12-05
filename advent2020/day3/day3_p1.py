#!/usr/bin/env python

def down_slope(slope):
    encountered_trees = 0
    right = 3
    down = 1
    while down < len(slope):
        vline = slope[down]
        # Add extra width if required
        if len(vline) <= right:
            mult = int(right / len(vline)) + 1
            vline *= mult
        # Did we find a tree?
        if vline[right] == '#':
            encountered_trees += 1
        # Keep going down and right
        down += 1
        right += 3

    print(encountered_trees)
    return


with open("input", "r") as input:
    in_list = input.read().splitlines()

down_slope(in_list)
