#!/usr/bin/env python3
"""Advent of Code 2015 Day 24 Part 2 — Balance with 4 groups.

Split into 4 equal groups; minimize group 1 size then QE.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from day24 import parse_weights, min_qe_for_groups


def solve(s: str) -> int:
    """Return minimal QE for the smallest first group in a 4-way split."""
    weights = parse_weights(s)
    return min_qe_for_groups(weights, 4)


if __name__ == "__main__":
    text = Path(__file__).with_name("d24_input.txt").read_text(encoding="utf-8")
    print(solve(text))
