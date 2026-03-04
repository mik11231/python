#!/usr/bin/env python
"""
advent2020/legacy/day2/day2_p2.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2020.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""


def check_passwords(input_list):
    """
    Run `check_passwords` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: input_list.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    valid_num = 0
    for password in input_list:
        elements = password.split(' ')
        count = elements[0].split('-')
        pos1 = int(count[0]) - 1
        pos2 = int(count[1]) - 1
        letter = elements[1].strip(':')
        pwd = elements[2]
        # Keep track of count in pwd
        letter_in_pwd = 0
        if pwd[pos1] is letter:
            letter_in_pwd += 1
        if pwd[pos2] is letter:
            letter_in_pwd += 1

        # Only valid if letter in password just recorded once at location
        if letter_in_pwd == 1:
            valid_num += letter_in_pwd

    print(valid_num)
    return


with open("input", "r") as input:
    in_list = input.read().splitlines()

check_passwords(in_list)
