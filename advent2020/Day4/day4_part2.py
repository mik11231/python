#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 4: Passport Processing (Part 2)

In addition to requiring all seven fields, each field value must now pass
strict validation rules:

    byr  - four digits, 1920-2002
    iyr  - four digits, 2010-2020
    eyr  - four digits, 2020-2030
    hgt  - a number followed by "cm" (150-193) or "in" (59-76)
    hcl  - '#' followed by exactly six hex digits
    ecl  - exactly one of: amb blu brn gry grn hzl oth
    pid  - exactly nine digits (including leading zeroes)
"""

import re
from pathlib import Path

from day4 import parse_passports, has_required_fields

VALID_EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def _in_range(value: str, lo: int, hi: int) -> bool:
    """Return True if *value* is an integer string within [lo, hi]."""
    try:
        return lo <= int(value) <= hi
    except ValueError:
        return False


def validate_byr(value: str) -> bool:
    return len(value) == 4 and _in_range(value, 1920, 2002)


def validate_iyr(value: str) -> bool:
    return len(value) == 4 and _in_range(value, 2010, 2020)


def validate_eyr(value: str) -> bool:
    return len(value) == 4 and _in_range(value, 2020, 2030)


def validate_hgt(value: str) -> bool:
    if value.endswith("cm"):
        return _in_range(value[:-2], 150, 193)
    if value.endswith("in"):
        return _in_range(value[:-2], 59, 76)
    return False


def validate_hcl(value: str) -> bool:
    return bool(re.fullmatch(r"#[0-9a-f]{6}", value))


def validate_ecl(value: str) -> bool:
    return value in VALID_EYE_COLORS


def validate_pid(value: str) -> bool:
    return len(value) == 9 and value.isdigit()


FIELD_VALIDATORS = {
    "byr": validate_byr,
    "iyr": validate_iyr,
    "eyr": validate_eyr,
    "hgt": validate_hgt,
    "hcl": validate_hcl,
    "ecl": validate_ecl,
    "pid": validate_pid,
}


def is_fully_valid(passport: dict[str, str]) -> bool:
    """Return True if *passport* has all required fields AND every field
    passes its validation rule."""
    if not has_required_fields(passport):
        return False
    return all(
        FIELD_VALIDATORS[field](passport[field]) for field in FIELD_VALIDATORS
    )


def solve(input_path: str = "advent2020/Day4/d4_input.txt") -> int:
    """Count passports that pass all field-level validation rules."""
    text = Path(input_path).read_text()
    passports = parse_passports(text)
    return sum(1 for p in passports if is_fully_valid(p))


if __name__ == "__main__":
    result = solve()
    print(f"Fully valid passports: {result}")
