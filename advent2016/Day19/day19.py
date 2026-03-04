#!/usr/bin/env python3
"""Advent of Code 2016 Day 19 Part 1: An Elephant Named Joseph."""

from pathlib import Path


def solve(s: str) -> int:
    """Return winner index for classic Josephus k=2."""
    n = int(s.strip())
    p = 1 << (n.bit_length() - 1)
    return 2 * (n - p) + 1


if __name__ == "__main__":
    text = Path(__file__).with_name("d19_input.txt").read_text(encoding="utf-8")
    print(solve(text))
