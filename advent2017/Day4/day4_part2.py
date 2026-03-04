#!/usr/bin/env python3
"""Advent of Code 2017 Day 4 Part 2."""

from pathlib import Path


def solve(s: str) -> int:
    out = 0
    for line in s.splitlines():
        w = ["".join(sorted(x)) for x in line.split()]
        out += int(len(set(w)) == len(w))
    return out


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d4_input.txt").read_text(encoding="utf-8")))
