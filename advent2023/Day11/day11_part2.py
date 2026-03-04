#!/usr/bin/env python3
"""Advent of Code 2023 Day 11 Part 2 — Cosmic Expansion.

Same as Part 1 but with an expansion factor of 1,000,000 instead of 2.
Reuses the galaxy_distances function from Part 1.
"""
from pathlib import Path
from day11 import galaxy_distances


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    return galaxy_distances(s, expansion=1_000_000)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d11_input.txt").read_text()))
