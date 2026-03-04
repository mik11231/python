#!/usr/bin/env python3
"""Advent of Code 2023 Day 1 Part 1 — Trebuchet?!

Each line contains a calibration value formed by combining the first digit
and the last digit (as characters) into a two-digit number. Return the sum
of all calibration values.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    total = 0
    for line in s.strip().splitlines():
        digits = [c for c in line if c.isdigit()]
        total += int(digits[0] + digits[-1])
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d1_input.txt").read_text()))
