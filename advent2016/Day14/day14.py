#!/usr/bin/env python3
"""Advent of Code 2016 Day 14 Part 1: One-Time Pad."""

from functools import lru_cache
import hashlib
from pathlib import Path


def triple(h: str) -> str | None:
    """Return first char appearing as a triple, if any."""
    for i in range(len(h) - 2):
        if h[i] == h[i + 1] == h[i + 2]:
            return h[i]
    return None


@lru_cache(maxsize=None)
def md5_hex(t: str) -> str:
    """Return MD5 hex digest."""
    return hashlib.md5(t.encode("utf-8")).hexdigest()


def solve(s: str) -> int:
    """Return index of 64th key using normal hashing."""
    salt = s.strip()
    keys = 0
    i = 0
    while True:
        h = md5_hex(f"{salt}{i}")
        c = triple(h)
        if c is not None:
            five = c * 5
            if any(five in md5_hex(f"{salt}{j}") for j in range(i + 1, i + 1001)):
                keys += 1
                if keys == 64:
                    return i
        i += 1


if __name__ == "__main__":
    text = Path(__file__).with_name("d14_input.txt").read_text(encoding="utf-8")
    print(solve(text))
