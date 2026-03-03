#!/usr/bin/env python3
"""Tests for Day 11 using the example from the problem statement.

Example layout (10×10):
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL

Part 1 (adjacent, threshold 4): 37 occupied seats at equilibrium.
Part 2 (line-of-sight, threshold 5): 26 occupied seats at equilibrium.
"""

from day11 import parse_grid, simulate, count_occupied
from day11_part2 import count_visible_occupied

EXAMPLE = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""


def test_part1():
    """Verify Part 1 example: 37 occupied seats at equilibrium (adjacent, threshold 4)."""
    grid = parse_grid(EXAMPLE)
    final = simulate(grid)
    result = count_occupied(final)
    assert result == 37, f"Expected 37 occupied seats, got {result}"
    print(f"PASS  Part 1: {result} occupied seats")


def test_part2():
    """Verify Part 2 example: 26 occupied seats at equilibrium (line-of-sight, threshold 5)."""
    grid = parse_grid(EXAMPLE)
    final = simulate(grid, neighbour_fn=count_visible_occupied, threshold=5)
    result = count_occupied(final)
    assert result == 26, f"Expected 26 occupied seats, got {result}"
    print(f"PASS  Part 2: {result} occupied seats")


if __name__ == "__main__":
    test_part1()
    test_part2()
    print("\nAll Day 11 tests passed!")
