#!/usr/bin/env python
"""
advent2020/legacy/day6/day6_p1.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2020.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""


def sum_answers(input):
    """
    Run `sum_answers` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: input.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    sum = 0
    for group in input:
        sum += len(set(group))
    return sum


with open("input", "r") as input:
    in_list = input.read().split("\n\n")
    for i in range(len(in_list)):
        in_list[i] = in_list[i].replace("\n", " ").replace(" ", "")

print(sum_answers(in_list))
