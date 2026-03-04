"""Geometry helpers shared across Advent of Code solutions."""

from __future__ import annotations


def manhattan2(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Return Manhattan distance between 2D points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def manhattan3(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    """Return Manhattan distance between 3D points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
