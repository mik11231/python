#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 2: Password Philosophy (Part 2)

The policy now describes two 1-based positions in the password.  Exactly one
of those positions must contain the given letter (not both, not neither).

    <pos1>-<pos2> <letter>: <password>
"""

from pathlib import Path

from day2 import parse_line


def is_valid_toboggan_policy(pos1: int, pos2: int, letter: str, password: str) -> bool:
    """Return True if exactly one of the two 1-based positions in *password*
    contains *letter*."""
    match_first = password[pos1 - 1] == letter
    match_second = password[pos2 - 1] == letter
    return match_first ^ match_second  # XOR: exactly one must match


def solve(input_path: str = "advent2020/Day2/d2_input.txt") -> int:
    """Count how many passwords satisfy the Toboggan Corporate policy."""
    lines = Path(input_path).read_text().splitlines()
    return sum(1 for line in lines if line.strip() and is_valid_toboggan_policy(*parse_line(line)))


if __name__ == "__main__":
    result = solve()
    print(f"Valid passwords (toboggan policy): {result}")
