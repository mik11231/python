#!/usr/bin/env python3
"""Advent of Code 2024 Day 3 Part 1 — Mull It Over.

Scan corrupted memory for valid mul(X,Y) instructions where X and Y are 1-3
digit numbers. Sum all their products. Uses a simple regex.
"""
import re
from pathlib import Path


def solve(s: str) -> int:
    """Return the sum of all valid mul(X,Y) products."""
    return sum(int(a) * int(b) for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", s))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d3_input.txt").read_text()))
