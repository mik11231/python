#!/usr/bin/env python3
"""Advent of Code 2017 Day 1 Part 2."""

from pathlib import Path


def solve(s: str) -> int:
    t = s.strip()
    k = len(t) // 2
    return sum(int(c) for i, c in enumerate(t) if c == t[(i + k) % len(t)])


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d1_input.txt").read_text(encoding="utf-8")))
