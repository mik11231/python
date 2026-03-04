#!/usr/bin/env python3
"""Advent of Code 2015 Day 1 Part 2 — Not Quite Lisp.

First position (1-indexed) where floor becomes -1.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Return 1-based index of first character that brings floor to -1."""
    floor = 0
    for i, ch in enumerate(s.strip(), start=1):
        floor += 1 if ch == "(" else -1
        if floor == -1:
            return i
    return -1


if __name__ == "__main__":
    text = Path(__file__).with_name("d1_input.txt").read_text(encoding="utf-8")
    print(solve(text))
