"""Advent of Code 2018 Day 25 has no separate computational Part 2.

Completing Part 1 unlocks the final star for the year.
This file exists to keep a consistent day/part file structure.
"""

from pathlib import Path
from day25 import solve, load


if __name__ == '__main__':
    # Re-run Part 1 answer for convenience/consistency.
    print(solve(load(Path(__file__).with_name('d25_input.txt'))))
