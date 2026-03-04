#!/usr/bin/env python3
"""Advent of Code 2024 Day 10 Part 2 - Hoof It.

Count the total number of distinct hiking trails (paths from any 0 to any 9
increasing by exactly 1). Uses memoised DFS: each cell caches how many
distinct trails lead from it to a 9.
"""
from pathlib import Path
from functools import lru_cache


def solve(s: str) -> int:
    """Return the sum of ratings (distinct trail counts) of all trailheads."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    heights = [[int(ch) for ch in row] for row in grid]

    @lru_cache(maxsize=None)
    def count_trails(r: int, c: int) -> int:
        if heights[r][c] == 9:
            return 1
        total = 0
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and heights[nr][nc] == heights[r][c] + 1):
                total += count_trails(nr, nc)
        return total

    return sum(
        count_trails(r, c)
        for r in range(rows) for c in range(cols)
        if heights[r][c] == 0
    )


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d10_input.txt").read_text()))
