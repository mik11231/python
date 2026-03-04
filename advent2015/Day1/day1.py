#!/usr/bin/env python3
"""Advent of Code 2015 Day 1 — Not Quite Lisp.

( = +1, ) = -1. Return final floor.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Return final floor after following parentheses."""
    return s.count("(") - s.count(")")


if __name__ == "__main__":
    text = Path(__file__).with_name("d1_input.txt").read_text(encoding="utf-8")
    print(solve(text))
