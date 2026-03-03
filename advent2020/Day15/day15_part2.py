#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 15: Rambunctious Recitation (Part 2)

Same memory game as Part 1, but now find the 30,000,000th number spoken.

Algorithm
---------
Reuses ``play_game`` from Part 1 — the dict-based approach is already O(1)
per turn, so 30 million iterations complete in a few seconds.
"""

from pathlib import Path

from day15 import play_game


def solve(input_path: str = "advent2020/Day15/d15_input.txt") -> int:
    """Read starting numbers and return the 30000000th number spoken."""
    text = Path(input_path).read_text().strip()
    starting = [int(n) for n in text.split(",")]
    return play_game(starting, 30_000_000)


if __name__ == "__main__":
    result = solve()
    print(f"The 30000000th number spoken: {result}")
