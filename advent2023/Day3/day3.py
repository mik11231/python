#!/usr/bin/env python3
"""Advent of Code 2023 Day 3 Part 1 — Gear Ratios.

Find all numbers in the engine schematic grid that are adjacent
(including diagonally) to any symbol (anything that is not a digit
and not a period). Return the sum of those part numbers.
"""
import re
from pathlib import Path


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    def has_adjacent_symbol(r: int, c_start: int, c_end: int) -> bool:
        """
        Run `has_adjacent_symbol` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: r, c_start, c_end.
        - Returns the computed result for this stage of the pipeline.
        """
        for dr in (-1, 0, 1):
            for c in range(c_start - 1, c_end + 1):
                nr = r + dr
                if 0 <= nr < rows and 0 <= c < cols:
                    ch = grid[nr][c]
                    if not ch.isdigit() and ch != ".":
                        return True
        return False

    total = 0
    for r, row in enumerate(grid):
        for m in re.finditer(r"\d+", row):
            if has_adjacent_symbol(r, m.start(), m.end()):
                total += int(m.group())
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d3_input.txt").read_text()))
