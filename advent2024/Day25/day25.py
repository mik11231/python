#!/usr/bin/env python3
"""Advent of Code 2024 Day 25 Part 1 - Code Chronicle.

Parse lock and key schematics (7-row, 5-column grids). Locks have '#' top row,
keys have '#' bottom row. Convert each to column heights, then count lock/key
pairs where no column sum exceeds 5.
"""
from pathlib import Path


def solve(s: str) -> int:
    blocks = s.strip().split('\n\n')
    locks, keys = [], []
    for block in blocks:
        rows = block.splitlines()
        heights = [sum(1 for r in rows if r[c] == '#') - 1 for c in range(5)]
        if rows[0] == '#####':
            locks.append(heights)
        else:
            keys.append(heights)

    count = 0
    for lock in locks:
        for key in keys:
            if all(lock[c] + key[c] <= 5 for c in range(5)):
                count += 1
    return count


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d25_input.txt").read_text()))
