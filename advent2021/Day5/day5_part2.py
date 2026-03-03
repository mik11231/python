#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 5: Hydrothermal Venture (Part 2)

Now include 45-degree diagonal line segments in addition to horizontal and
vertical ones.  Count the number of points where at least two lines overlap.

Algorithm
---------
Same approach as Part 1 but with ``include_diagonal=True`` so that diagonal
segments are also expanded into their constituent points.
"""

from pathlib import Path

from day5 import parse_lines, count_overlaps


def solve(input_path: str = "advent2021/Day5/d5_input.txt") -> int:
    """Read vent lines and return overlap count including diagonals."""
    segments = parse_lines(Path(input_path).read_text())
    return count_overlaps(segments, include_diagonal=True)


if __name__ == "__main__":
    result = solve()
    print(f"Overlapping points (incl. diagonals): {result}")
