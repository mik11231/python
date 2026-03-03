#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 9: Smoke Basin (Part 2)

Basins are regions that flow down to a single low point.  Positions with
height 9 are barriers and belong to no basin.  Find the three largest
basins and return the product of their sizes.

Algorithm
---------
BFS / flood-fill from each low point, expanding to orthogonal neighbors
whose height is not 9.  Track visited cells globally so no cell is counted
twice.  Sort the resulting basin sizes and multiply the three largest.
O(rows × cols).
"""

from collections import deque
from math import prod
from pathlib import Path

from day9 import parse_grid, find_low_points


def basin_sizes(grid: list[list[int]]) -> list[int]:
    """Return the size of every basin, one per low point."""
    rows, cols = len(grid), len(grid[0])
    visited: set[tuple[int, int]] = set()
    sizes: list[int] = []

    for r, c, _ in find_low_points(grid):
        queue: deque[tuple[int, int]] = deque([(r, c)])
        size = 0
        while queue:
            cr, cc = queue.popleft()
            if (cr, cc) in visited:
                continue
            if grid[cr][cc] == 9:
                continue
            visited.add((cr, cc))
            size += 1
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                    queue.append((nr, nc))
        sizes.append(size)

    return sizes


def solve(input_path: str = "advent2021/Day9/d9_input.txt") -> int:
    """Read the heightmap and return the product of the three largest basins."""
    text = Path(input_path).read_text()
    grid = parse_grid(text)
    sizes = sorted(basin_sizes(grid), reverse=True)
    return prod(sizes[:3])


if __name__ == "__main__":
    result = solve()
    print(f"Product of the three largest basin sizes: {result}")
