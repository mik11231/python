#!/usr/bin/env python3
"""Advent of Code 2015 Day 2 — I Was Told There Would Be No Math.

Surface area 2*l*w+2*w*h+2*h*l plus area of smallest side.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines, ints


def solve(s: str) -> int:
    """Sum wrapping paper area for each line l x w x h."""
    total = 0
    for line in lines(s):
        dims = sorted(ints(line))
        if len(dims) != 3:
            continue
        l, w, h = dims
        area = 2 * l * w + 2 * w * h + 2 * h * l
        slack = l * w
        total += area + slack
    return total


if __name__ == "__main__":
    text = Path(__file__).with_name("d2_input.txt").read_text(encoding="utf-8")
    print(solve(text))
