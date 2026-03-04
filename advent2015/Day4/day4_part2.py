#!/usr/bin/env python3
"""Advent of Code 2015 Day 4 Part 2 — Six zero hex digits."""
import hashlib
from pathlib import Path


def solve(s: str) -> int:
    """Return smallest positive n such that MD5(secret+n) starts with 000000."""
    secret = s.strip()
    n = 0
    while True:
        n += 1
        h = hashlib.md5((secret + str(n)).encode()).hexdigest()
        if h.startswith("000000"):
            return n
    return -1


if __name__ == "__main__":
    text = Path(__file__).with_name("d4_input.txt").read_text(encoding="utf-8")
    print(solve(text))
