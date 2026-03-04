#!/usr/bin/env python3
r"""Advent of Code 2015 Day 8 Part 2 — Encoded length.

New encoding: " becomes \", \ becomes \\. Sum (encoded length - literal length).
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines


def solve(s: str) -> int:
    """Return sum of (encoded length - literal length) per line."""
    total = 0
    for line in lines(s):
        line = line.strip()
        if not line:
            continue
        literal = len(line)
        encoded = 2  # outer quotes
        for c in line:
            if c == '"' or c == "\\":
                encoded += 2
            else:
                encoded += 1
        total += encoded - literal
    return total


if __name__ == "__main__":
    text = Path(__file__).with_name("d8_input.txt").read_text(encoding="utf-8")
    print(solve(text))
