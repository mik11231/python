#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 5: Hydrothermal Venture (Part 1)

Map hydrothermal vent lines on the ocean floor.  Each line is defined by its
two endpoints.  For Part 1 consider only horizontal and vertical lines and
count the number of points where at least two lines overlap.

Algorithm
---------
Parse each line segment, generate every integer point on horizontal/vertical
segments using ``range``, and count occurrences with a ``Counter``.  Points
with count ≥ 2 are the answer.
"""

from collections import Counter
from pathlib import Path


def parse_lines(text: str) -> list[tuple[int, int, int, int]]:
    """Parse line segments from input text.

    Returns a list of (x1, y1, x2, y2) tuples.
    """
    segments: list[tuple[int, int, int, int]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        left, right = line.split(" -> ")
        x1, y1 = (int(v) for v in left.split(","))
        x2, y2 = (int(v) for v in right.split(","))
        segments.append((x1, y1, x2, y2))
    return segments


def _sign(n: int) -> int:
    return (n > 0) - (n < 0)


def points_on_segment(x1: int, y1: int, x2: int, y2: int,
                       include_diagonal: bool = False) -> list[tuple[int, int]]:
    """Return all integer points on the segment (x1,y1)→(x2,y2).

    Only horizontal/vertical segments are expanded unless
    *include_diagonal* is True (for 45° diagonals).
    """
    dx = _sign(x2 - x1)
    dy = _sign(y2 - y1)
    if not include_diagonal and dx != 0 and dy != 0:
        return []
    points: list[tuple[int, int]] = []
    x, y = x1, y1
    while True:
        points.append((x, y))
        if x == x2 and y == y2:
            break
        x += dx
        y += dy
    return points


def count_overlaps(segments: list[tuple[int, int, int, int]],
                   include_diagonal: bool = False) -> int:
    """Return the number of points where at least two segments overlap."""
    counter: Counter[tuple[int, int]] = Counter()
    for x1, y1, x2, y2 in segments:
        for pt in points_on_segment(x1, y1, x2, y2, include_diagonal):
            counter[pt] += 1
    return sum(1 for v in counter.values() if v >= 2)


def solve(input_path: str = "advent2021/Day5/d5_input.txt") -> int:
    """Read vent lines and return the number of dangerous overlap points."""
    segments = parse_lines(Path(input_path).read_text())
    return count_overlaps(segments, include_diagonal=False)


if __name__ == "__main__":
    result = solve()
    print(f"Overlapping points (H/V only): {result}")
