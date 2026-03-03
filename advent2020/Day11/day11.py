#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 11: Seating System (Part 1)

Cellular automaton on a seat layout:
  - ``L`` = empty seat, ``#`` = occupied seat, ``.`` = floor (never changes).
  - All rules are applied simultaneously each step:
      * Empty seat with **0** occupied neighbours -> becomes occupied.
      * Occupied seat with **4+** occupied neighbours -> becomes empty.
  - Repeat until the layout stabilises.  Count occupied seats.

Algorithm
---------
Store the grid as a list-of-lists.  Each tick, build a new grid by applying
the rules cell-by-cell, checking the 8 adjacent cells.  Stop when two
consecutive grids are identical.
"""

from pathlib import Path

Grid = list[list[str]]

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              ( 0, -1),          ( 0, 1),
              ( 1, -1), ( 1, 0), ( 1, 1)]


def parse_grid(text: str) -> Grid:
    """Parse the seat layout into a 2-D list of characters."""
    return [list(line) for line in text.splitlines() if line.strip()]


def count_adjacent_occupied(grid: Grid, row: int, col: int) -> int:
    """Count occupied seats in the 8 cells immediately adjacent to (row, col)."""
    rows, cols = len(grid), len(grid[0])
    count = 0
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols and grid[r][c] == "#":
            count += 1
    return count


def step(grid: Grid, neighbour_fn=None, threshold: int = 4) -> Grid:
    """Apply one round of seating rules and return the new grid.

    *neighbour_fn(grid, row, col)* counts occupied neighbours (defaults to
    ``count_adjacent_occupied``).  *threshold* is the minimum occupied
    neighbours that cause a seat to empty.
    """
    if neighbour_fn is None:
        neighbour_fn = count_adjacent_occupied
    rows, cols = len(grid), len(grid[0])
    new_grid: Grid = [row[:] for row in grid]

    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            if cell == "L" and neighbour_fn(grid, r, c) == 0:
                new_grid[r][c] = "#"
            elif cell == "#" and neighbour_fn(grid, r, c) >= threshold:
                new_grid[r][c] = "L"

    return new_grid


def simulate(grid: Grid, neighbour_fn=None, threshold: int = 4) -> Grid:
    """Run the automaton until the layout stabilises and return the final grid."""
    while True:
        new_grid = step(grid, neighbour_fn, threshold)
        if new_grid == grid:
            return grid
        grid = new_grid


def count_occupied(grid: Grid) -> int:
    """Count all ``#`` cells in the grid."""
    return sum(cell == "#" for row in grid for cell in row)


def solve(input_path: str = "advent2020/Day11/d11_input.txt") -> int:
    """Read the seat layout, simulate until stable, and return the number
    of occupied seats."""
    grid = parse_grid(Path(input_path).read_text())
    final = simulate(grid)
    return count_occupied(final)


if __name__ == "__main__":
    result = solve()
    print(f"Occupied seats at equilibrium (Part 1): {result}")
