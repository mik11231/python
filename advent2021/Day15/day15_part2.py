#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 15: Chiton (Part 2)

The full cave is 5 times larger in each dimension.  Each tile is the
original grid with risk levels incremented by (tile_row + tile_col),
wrapping 9 -> 1.  Run Dijkstra on the expanded grid.

Algorithm
---------
Build the 5x-tiled grid using modular arithmetic for the risk wrap-around,
then reuse the Dijkstra implementation from Part 1.
"""

from pathlib import Path

from day15 import parse_grid, dijkstra


def expand_grid(grid: list[list[int]], factor: int = 5) -> list[list[int]]:
    """Tile *grid* into a *factor* x *factor* super-grid with wrapping risk."""
    rows, cols = len(grid), len(grid[0])
    big: list[list[int]] = []
    for tr in range(factor):
        for r in range(rows):
            row: list[int] = []
            for tc in range(factor):
                for c in range(cols):
                    val = grid[r][c] + tr + tc
                    row.append((val - 1) % 9 + 1)
            big.append(row)
    return big


def solve(input_path: str = "advent2021/Day15/d15_input.txt") -> int:
    """Read puzzle input, expand the grid 5x5, and return the lowest risk."""
    grid = parse_grid(Path(input_path).read_text())
    return dijkstra(expand_grid(grid))


if __name__ == "__main__":
    result = solve()
    print(f"Lowest total risk (5x grid): {result}")
