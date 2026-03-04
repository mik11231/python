#!/usr/bin/env python3
"""Advent of Code 2017 Day 13 Part 2."""

from pathlib import Path


def solve(s: str) -> int:
    layers = []
    for ln in s.splitlines():
        d, r = map(int, ln.split(": "))
        layers.append((d, 2 * (r - 1)))
    t = 0
    while True:
        if all((t + d) % cyc != 0 for d, cyc in layers):
            return t
        t += 1


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d13_input.txt").read_text(encoding="utf-8")))
