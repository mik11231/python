#!/usr/bin/env python3
"""Tests for Day 5 using the example from the problem statement.

Example 10 line segments (see EXAMPLE_TEXT).

Part 1 (H/V only): 5 points with at least two overlapping lines.
Part 2 (incl. diagonals): 12 points with at least two overlapping lines.
"""

from day5 import parse_lines, count_overlaps

EXAMPLE_TEXT = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 2,2
"""


def test_part1():
    """Verify Part 1: 5 overlap points with horizontal/vertical lines only."""
    segments = parse_lines(EXAMPLE_TEXT)
    assert count_overlaps(segments, include_diagonal=False) == 5


def test_part2():
    """Verify Part 2: 12 overlap points including diagonal lines."""
    segments = parse_lines(EXAMPLE_TEXT)
    assert count_overlaps(segments, include_diagonal=True) == 12


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 5 overlapping points")
    test_part2()
    print("PASS  Part 2: 12 overlapping points")
    print("\nAll Day 5 tests passed!")
