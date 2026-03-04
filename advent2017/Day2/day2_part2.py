#!/usr/bin/env python3
"""Advent of Code 2017 Day 2 Part 2."""

from pathlib import Path


def solve(s: str) -> int:
    total = 0
    for line in s.splitlines():
        if not line.strip():
            continue
        vals = list(map(int, line.split()))
        found = False
        for i, a in enumerate(vals):
            for j, b in enumerate(vals):
                if i != j and a % b == 0:
                    total += a // b
                    found = True
                    break
            if found:
                break
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d2_input.txt").read_text(encoding="utf-8")))
