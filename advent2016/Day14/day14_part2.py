#!/usr/bin/env python3
"""Advent of Code 2016 Day 14 Part 2: stretched hashes."""

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
def stretched(t: str) -> str:
    """Return 2017-times-rehashed MD5 hex digest."""
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    for _ in range(2016):
        h = hashlib.md5(h.encode("utf-8")).hexdigest()
    return h


def solve(s: str) -> int:
    """Return index of 64th key using stretched hashing."""
    salt = s.strip()
    keys = 0
    i = 0
    while True:
        h = stretched(f"{salt}{i}")
        c = triple(h)
        if c is not None:
            five = c * 5
            if any(five in stretched(f"{salt}{j}") for j in range(i + 1, i + 1001)):
                keys += 1
                if keys == 64:
                    return i
        i += 1


if __name__ == "__main__":
    text = Path(__file__).with_name("d14_input.txt").read_text(encoding="utf-8")
    print(solve(text))
