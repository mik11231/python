#!/usr/bin/env python
"""
advent2020/legacy/day3/day3_p1.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2020.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""


def down_slope(slope):
    """
    Run `down_slope` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: slope.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
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
