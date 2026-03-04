#!/usr/bin/env python3
"""Advent of Code 2023 Day 13 Part 1 — Point of Incidence.

Find lines of reflection in each pattern.  For each candidate axis, count
mismatches across the mirror; Part 1 requires exactly 0 mismatches.
Vertical lines contribute columns-left; horizontal lines contribute 100*rows-above.
"""
from pathlib import Path


def find_reflection(grid: list[str], target_smudges: int = 0) -> int:
    """Return the summary value for one pattern."""
    rows, cols = len(grid), len(grid[0])

    for c in range(1, cols):
        smudges = 0
        for r in range(rows):
            for dc in range(min(c, cols - c)):
                if grid[r][c - 1 - dc] != grid[r][c + dc]:
                    smudges += 1
        if smudges == target_smudges:
            return c

    for r in range(1, rows):
        smudges = 0
        for dr in range(min(r, rows - r)):
            for c in range(cols):
                if grid[r - 1 - dr][c] != grid[r + dr][c]:
                    smudges += 1
        if smudges == target_smudges:
            return 100 * r

    return 0


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    return sum(
        find_reflection(block.splitlines())
        for block in s.strip().split("\n\n")
    )


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d13_input.txt").read_text()))
