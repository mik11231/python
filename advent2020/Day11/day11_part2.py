#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 11: Seating System (Part 2)

Same automaton, different neighbour rule:
  - Instead of checking the 8 immediately adjacent cells, look along each
    of the 8 directions until you see the **first seat** (``L`` or ``#``),
    skipping floor tiles (``.``).
  - The crowding threshold rises from 4 to **5**.

Algorithm
---------
Reuse ``simulate`` from Part 1 with a custom ``count_visible_occupied``
function and threshold = 5.
"""

from pathlib import Path

from day11 import Grid, DIRECTIONS, parse_grid, simulate, count_occupied


def count_visible_occupied(grid: Grid, row: int, col: int) -> int:
    """Count occupied seats visible from (row, col) by ray-casting in
    each of the 8 directions until a seat (or the edge) is found."""
    rows, cols = len(grid), len(grid[0])
    count = 0
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols:
            if grid[r][c] == "#":
                count += 1
                break
            if grid[r][c] == "L":
                break
            r += dr
            c += dc
    return count


def solve(input_path: str = "advent2020/Day11/d11_input.txt") -> int:
    """Read the seat layout, simulate with line-of-sight rules, and return
    the number of occupied seats at equilibrium."""
    grid = parse_grid(Path(input_path).read_text())
    final = simulate(grid, neighbour_fn=count_visible_occupied, threshold=5)
    return count_occupied(final)


if __name__ == "__main__":
    result = solve()
    print(f"Occupied seats at equilibrium (Part 2): {result}")
