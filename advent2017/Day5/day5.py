#!/usr/bin/env python3
"""Advent of Code 2017 Day 5 Part 1."""

from pathlib import Path


def solve(s: str) -> int:
    a = [int(x) for x in s.split()]
    i = 0
    steps = 0
    n = len(a)
    while 0 <= i < n:
        j = a[i]
        a[i] += 1
        i += j
        steps += 1
    return steps


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d5_input.txt").read_text(encoding="utf-8")))
