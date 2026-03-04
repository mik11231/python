#!/usr/bin/env python
"""
advent2020/legacy/day1/day1_p1.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2020.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""


def fix_expense(input_list):
    """
    Run `fix_expense` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: input_list.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    for first_num in input_list:
        for second_num in input_list:
            sum = int(first_num) + int(second_num)
            if sum == 2020:
                print(int(first_num) * int(second_num))
                return


with open("input", "r") as input:
    in_list = input.read().splitlines()


fix_expense(in_list)
