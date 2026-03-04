#!/usr/bin/env python3
"""Advent of Code 2016 Day 16 Part 1: Dragon Checksum."""

from pathlib import Path


def fill(seed: str, n: int) -> str:
    """Generate dragon curve data truncated to length n."""
    a = seed
    while len(a) < n:
        b = "".join("1" if ch == "0" else "0" for ch in reversed(a))
        a = a + "0" + b
    return a[:n]


def checksum(data: str) -> str:
    """Compute repeated pairwise checksum until odd length."""
    c = data
    while len(c) % 2 == 0:
        c = "".join("1" if c[i] == c[i + 1] else "0" for i in range(0, len(c), 2))
    return c


def solve(s: str) -> str:
    """Return checksum for disk length 272."""
    return checksum(fill(s.strip(), 272))


if __name__ == "__main__":
    text = Path(__file__).with_name("d16_input.txt").read_text(encoding="utf-8")
    print(solve(text))
