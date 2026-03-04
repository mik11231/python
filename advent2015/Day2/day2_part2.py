#!/usr/bin/env python3
"""Advent of Code 2015 Day 2 Part 2 — Ribbon.

Smallest perimeter of any two sides plus volume l*w*h.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines, ints


def solve(s: str) -> int:
    """Sum ribbon length for each line l x w x h."""
    total = 0
    for line in lines(s):
        dims = sorted(ints(line))
        if len(dims) != 3:
            continue
        l, w, h = dims
        ribbon = 2 * l + 2 * w
        bow = l * w * h
        total += ribbon + bow
    return total


if __name__ == "__main__":
    text = Path(__file__).with_name("d2_input.txt").read_text(encoding="utf-8")
    print(solve(text))
