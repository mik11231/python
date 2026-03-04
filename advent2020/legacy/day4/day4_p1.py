#!/usr/bin/env python
"""
advent2020/legacy/day4/day4_p1.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2020.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""


def validate_passport(pas_list):
    """
    Run `validate_passport` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: pas_list.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    valid_passport = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    valid_passport_count = 0
    for passport in pas_list:
        if valid_passport.issubset(passport.keys()):
            valid_passport_count += 1
    return valid_passport_count


with open("input", "r") as input:
    in_list = input.read().split("\n\n")
    for i in range(len(in_list)):
        in_list[i] = in_list[i].replace("\n", " ")
        passport_dict = {}
        for element in in_list[i].split(" "):
            passport_data = element.split(":")
            if len(passport_data) == 2:
                passport_dict[passport_data[0]] = passport_data[1]
        in_list[i] = passport_dict

print(validate_passport(in_list))
