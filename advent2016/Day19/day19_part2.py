#!/usr/bin/env python3
"""Advent of Code 2016 Day 19 Part 2: opposite-stealing variant."""

from pathlib import Path


def solve(s: str) -> int:
    """Return winner using base-3 closed form for opposite removal game."""
    n = int(s.strip())
    p = 1
    while p * 3 <= n:
        p *= 3
    if n == p:
        return n
    if n <= 2 * p:
        return n - p
    return 2 * n - 3 * p


if __name__ == "__main__":
    text = Path(__file__).with_name("d19_input.txt").read_text(encoding="utf-8")
    print(solve(text))
