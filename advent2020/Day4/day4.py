#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 4: Passport Processing (Part 1)

Passports are separated by blank lines.  Each passport is a set of
key:value pairs (space- or newline-delimited).

A passport is valid when it contains all seven required fields:
    byr, iyr, eyr, hgt, hcl, ecl, pid
The optional field `cid` (Country ID) may be missing.
"""

from pathlib import Path

REQUIRED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


def parse_passports(text: str) -> list[dict[str, str]]:
    """Split raw input on blank lines and parse each passport into a dict."""
    passports: list[dict[str, str]] = []
    for block in text.split("\n\n"):
        tokens = block.replace("\n", " ").split()
        passport = {}
        for token in tokens:
            key, _, value = token.partition(":")
            if key:
                passport[key] = value
        passports.append(passport)
    return passports


def has_required_fields(passport: dict[str, str]) -> bool:
    """Return True if *passport* contains every required field."""
    return REQUIRED_FIELDS.issubset(passport.keys())


def solve(input_path: str = "advent2020/Day4/d4_input.txt") -> int:
    """Count passports that have all required fields (field values unchecked)."""
    text = Path(input_path).read_text()
    passports = parse_passports(text)
    return sum(1 for p in passports if has_required_fields(p))


if __name__ == "__main__":
    result = solve()
    print(f"Passports with all required fields: {result}")
