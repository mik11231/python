#!/usr/bin/env python3
"""Shared helpers for Advent of Code 2024 Day 20 solutions."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.grid import neighbors4
from aoclib.search import bfs_distances

Cell = tuple[int, int]


def parse_track(s: str) -> tuple[list[str], Cell, Cell]:
    """Parse grid text and return (grid_lines, start_cell, end_cell)."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    start: Cell | None = None
    end: Cell | None = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)

    if start is None or end is None:
        raise ValueError("Track must contain both S (start) and E (end) cells.")
    return grid, start, end


def track_distances(grid: list[str], start: Cell) -> dict[Cell, int]:
    """Return BFS distance to every walkable track cell from start."""
    rows, cols = len(grid), len(grid[0])

    def _neighbors(cell: Cell):
        """
        Run `_neighbors` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: cell.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        r, c = cell
        for nr, nc in neighbors4(r, c, rows, cols):
            if grid[nr][nc] != "#":
                yield (nr, nc)

    return bfs_distances(start, _neighbors)
