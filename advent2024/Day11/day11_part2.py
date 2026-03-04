#!/usr/bin/env python3
"""Advent of Code 2024 Day 11 Part 2 - Plutonian Pebbles.

Same rules as Part 1 but simulated for 75 blinks. The dict-based counting
keeps the computation tractable despite exponential stone growth.
"""
from pathlib import Path
from collections import Counter
from day11 import blink


def solve(s: str) -> int:
    """Return number of stones after 75 blinks."""
    stones = Counter(map(int, s.strip().split()))
    return sum(blink(stones, 75).values())


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d11_input.txt").read_text()))
