#!/usr/bin/env python3
"""Advent of Code 2015 Day 4 — The Ideal Stocking Stuffer.

Find lowest positive number such that MD5(secret+number) has 5 zero hex digits.
"""
import hashlib
from pathlib import Path


def solve(s: str, prefix: str = "00000") -> int:
    """Return smallest positive n such that MD5(secret+n) starts with prefix."""
    secret = s.strip()
    n = 0
    while True:
        n += 1
        h = hashlib.md5((secret + str(n)).encode()).hexdigest()
        if h.startswith(prefix):
            return n
    return -1


if __name__ == "__main__":
    text = Path(__file__).with_name("d4_input.txt").read_text(encoding="utf-8")
    print(solve(text))
