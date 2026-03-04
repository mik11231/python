#!/usr/bin/env python3
"""Advent of Code 2016 Day 9 Part 2: recursive decompression length."""

from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=None)
def dec_len(t: str) -> int:
    """Return recursively decompressed length of string segment."""
    i = 0
    out = 0
    while i < len(t):
        if t[i] != "(":
            out += 1
            i += 1
            continue
        j = t.index(")", i)
        a, b = map(int, t[i + 1 : j].split("x"))
        seg = t[j + 1 : j + 1 + a]
        out += b * dec_len(seg)
        i = j + 1 + a
    return out


def solve(s: str) -> int:
    """Return full recursive decompressed length."""
    return dec_len(s.strip())


if __name__ == "__main__":
    text = Path(__file__).with_name("d9_input.txt").read_text(encoding="utf-8")
    print(solve(text))
