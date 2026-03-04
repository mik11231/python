#!/usr/bin/env python3
"""Advent of Code 2016 Day 5 Part 1: How About a Nice Game of Chess?"""

import hashlib
from pathlib import Path


def solve(s: str) -> str:
    """Compute first password by collecting 6th hex char of qualifying MD5 hashes."""
    door = s.strip()
    i = 0
    pw: list[str] = []
    while len(pw) < 8:
        h = hashlib.md5(f"{door}{i}".encode("utf-8")).hexdigest()
        if h.startswith("00000"):
            pw.append(h[5])
        i += 1
    return "".join(pw)


if __name__ == "__main__":
    text = Path(__file__).with_name("d5_input.txt").read_text(encoding="utf-8")
    print(solve(text))
