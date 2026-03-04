"""Grid utilities for 2D Advent of Code problems."""

from __future__ import annotations

from typing import Iterable, Iterator


DIR4: tuple[tuple[int, int], ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIR8: tuple[tuple[int, int], ...] = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
)


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    """Return True when (r, c) is within [0, rows) x [0, cols)."""
    return 0 <= r < rows and 0 <= c < cols


def neighbors4(r: int, c: int, rows: int, cols: int) -> Iterator[tuple[int, int]]:
    """Yield in-bounds 4-directional neighbors."""
    for dr, dc in DIR4:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc, rows, cols):
            yield nr, nc


def neighbors8(r: int, c: int, rows: int, cols: int) -> Iterator[tuple[int, int]]:
    """Yield in-bounds 8-directional neighbors."""
    for dr, dc in DIR8:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc, rows, cols):
            yield nr, nc


def find_cells(grid: list[list[str]], target: str) -> list[tuple[int, int]]:
    """Return all cell coordinates containing target."""
    out: list[tuple[int, int]] = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == target:
                out.append((r, c))
    return out


def to_lines(grid: list[list[str]]) -> list[str]:
    """Convert char grid back to text lines."""
    return ["".join(row) for row in grid]
