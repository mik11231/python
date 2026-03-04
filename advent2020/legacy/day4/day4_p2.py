#!/usr/bin/env python
"""
advent2020/legacy/day4/day4_p2.py

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
            if not validate_byr(passport["byr"]):
                continue
            if not validate_iyr(passport["iyr"]):
                continue
            if not validate_eyr(passport["eyr"]):
                continue
            if not validate_hgt(passport["hgt"]):
                continue
            if not validate_hcl(passport["hcl"]):
                continue
            if not validate_ecl(passport["ecl"]):
                continue
            if not validate_pid(passport["pid"]):
                continue
            valid_passport_count += 1
    return valid_passport_count


def check_range(num, least, most):
    """
    Run `check_range` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: num, least, most.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    try:
        num = int(num)
        if (num >= least) and (num <= most):
            return True
        else:
            return False
    except Exception:
        return False


def validate_byr(byr):
    """
    Run `validate_byr` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: byr.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    return check_range(byr, 1920, 2002)


def validate_iyr(iyr):
    """
    Run `validate_iyr` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: iyr.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    return check_range(iyr, 2010, 2020)


def validate_eyr(eyr):
    """
    Run `validate_eyr` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: eyr.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    return check_range(eyr, 2020, 2030)


def validate_hgt(hgt):
    """
    Run `validate_hgt` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: hgt.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    if "cm" in hgt:
        height = hgt.strip("cm")
        return check_range(height, 150, 193)
    elif "in" in hgt:
        height = hgt.strip("in")
        return check_range(height, 59, 76)
    else:
        return False


def validate_hcl(hcl):
    """
    Run `validate_hcl` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: hcl.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    if (hcl[0] == "#") and (len(hcl) == 7):
        color = hcl.strip("#")
        try:
            int(color, 16)
            return True
        except ValueError:
            return False
    else:
        return False


def validate_ecl(ecl):
    """
    Run `validate_ecl` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: ecl.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    valid_colors = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    color = set([ecl])
    return color.issubset(valid_colors)


def validate_pid(pid):
    """
    Run `validate_pid` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: pid.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    if (len(pid) == 9) and pid.isdigit():
        return True
    else:
        return False


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
