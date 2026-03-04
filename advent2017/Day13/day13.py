#!/usr/bin/env python3
"""Advent of Code 2017 Day 13 Part 1."""

from pathlib import Path


def solve(s: str) -> int:
    sev = 0
    for ln in s.splitlines():
        d, r = map(int, ln.split(": "))
        cyc = 2 * (r - 1)
        if d % cyc == 0:
            sev += d * r
    return sev


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d13_input.txt").read_text(encoding="utf-8")))
