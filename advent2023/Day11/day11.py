#!/usr/bin/env python3
"""Advent of Code 2023 Day 11 Part 1 — Cosmic Expansion.

Find galaxies (#), expand empty rows/columns by factor 2, then compute the
sum of Manhattan distances between all pairs.  Uses coordinate remapping
instead of actually expanding the grid.
"""
from pathlib import Path
from itertools import combinations
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.geometry import manhattan2


def galaxy_distances(s: str, expansion: int = 2) -> int:
    """Return sum of shortest paths between all galaxy pairs."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    empty_rows = {r for r in range(rows) if all(grid[r][c] == "." for c in range(cols))}
    empty_cols = {c for c in range(cols) if all(grid[r][c] == "." for r in range(rows))}

    galaxies: list[tuple[int, int]] = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "#":
                er = sum(1 for er in empty_rows if er < r)
                ec = sum(1 for ec in empty_cols if ec < c)
                galaxies.append((r + er * (expansion - 1), c + ec * (expansion - 1)))

    return sum(
        manhattan2(a, b)
        for a, b in combinations(galaxies, 2)
    )


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    return galaxy_distances(s, expansion=2)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d11_input.txt").read_text()))
