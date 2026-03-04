#!/usr/bin/env python3
"""Advent of Code 2016 Day 2 Part 1: Bathroom Security."""

from pathlib import Path


def solve(s: str) -> str:
    """Return bathroom code on the 3x3 keypad."""
    r, c = 1, 1
    code: list[str] = []
    for line in s.splitlines():
        for ch in line.strip():
            if ch == "U":
                r = max(0, r - 1)
            elif ch == "D":
                r = min(2, r + 1)
            elif ch == "L":
                c = max(0, c - 1)
            elif ch == "R":
                c = min(2, c + 1)
        code.append(str(r * 3 + c + 1))
    return "".join(code)


if __name__ == "__main__":
    text = Path(__file__).with_name("d2_input.txt").read_text(encoding="utf-8")
    print(solve(text))
