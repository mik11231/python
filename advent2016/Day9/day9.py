#!/usr/bin/env python3
"""Advent of Code 2016 Day 9 Part 1: Explosives in Cyberspace."""

from pathlib import Path


def solve(s: str) -> int:
    """Return decompressed length (non-recursive marker expansion)."""
    t = s.strip()
    i = 0
    out = 0
    while i < len(t):
        if t[i] != "(":
            out += 1
            i += 1
            continue
        j = t.index(")", i)
        a, b = map(int, t[i + 1 : j].split("x"))
        out += a * b
        i = j + 1 + a
    return out


if __name__ == "__main__":
    text = Path(__file__).with_name("d9_input.txt").read_text(encoding="utf-8")
    print(solve(text))
