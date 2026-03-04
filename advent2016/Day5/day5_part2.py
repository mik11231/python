#!/usr/bin/env python3
"""Advent of Code 2016 Day 5 Part 2: positional MD5 password."""

import hashlib
from pathlib import Path


def solve(s: str) -> str:
    """Compute second password using hash-derived positions."""
    door = s.strip()
    i = 0
    pw = ["_"] * 8
    filled = 0
    while filled < 8:
        h = hashlib.md5(f"{door}{i}".encode("utf-8")).hexdigest()
        if h.startswith("00000") and h[5].isdigit():
            pos = int(h[5])
            if pos < 8 and pw[pos] == "_":
                pw[pos] = h[6]
                filled += 1
        i += 1
    return "".join(pw)


if __name__ == "__main__":
    text = Path(__file__).with_name("d5_input.txt").read_text(encoding="utf-8")
    print(solve(text))
