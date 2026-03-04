#!/usr/bin/env python
"""
advent2020/legacy/day5/day5_p1.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2020.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""


def highest_id(input):
    """
    Run `highest_id` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: input.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    id = 0
    for seat in input:
        tmp_id = seat[0] * 8 + seat[1]
        if tmp_id > id:
            id = tmp_id
    return id


with open("input", "r") as input:
    in_list = input.read().splitlines()
    seat = []
    for i in range(len(in_list)):
        row = in_list[i][0:7].replace("F", "0").replace("B", "1")
        column = in_list[i][7:10].replace("R", "1").replace("L", "0")
        seat = [int(row, 2), int(column, 2)]
        in_list[i] = seat

print(highest_id(in_list))
