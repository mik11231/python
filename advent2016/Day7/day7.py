#!/usr/bin/env python3
"""Advent of Code 2016 Day 7 Part 1: Internet Protocol Version 7."""

from pathlib import Path
import re


def has_abba(t: str) -> bool:
    """Return whether text contains an ABBA pattern."""
    for i in range(len(t) - 3):
        a, b, c, d = t[i : i + 4]
        if a != b and a == d and b == c:
            return True
    return False


def solve(s: str) -> int:
    """Count IPs supporting TLS."""
    total = 0
    for line in s.splitlines():
        parts = re.split(r"\[|\]", line.strip())
        outs = parts[0::2]
        ins = parts[1::2]
        if any(has_abba(x) for x in outs) and not any(has_abba(x) for x in ins):
            total += 1
    return total


if __name__ == "__main__":
    text = Path(__file__).with_name("d7_input.txt").read_text(encoding="utf-8")
    print(solve(text))
