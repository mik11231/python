#!/usr/bin/env python

def down_slope(slope, right, down):
    encountered_trees = 0
    right_count = right
    down_count = down
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
        down += down_count
        right += right_count

    return encountered_trees


with open("input", "r") as input:
    in_list = input.read().splitlines()

paths = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
multi_trees = 1
for path in paths:
    right_num = path[0]
    down_num = path[1]
    multi_trees *= down_slope(in_list, right_num, down_num)
print(multi_trees)
