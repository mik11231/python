#!/usr/bin/env python3
"""Tests for Day 3 using the example from the problem statement.

The 11-wide map repeats horizontally.  For slope right-3 down-1 the answer
is 7 trees.  The product of all five slopes is 336.
"""

from day3 import count_trees

EXAMPLE_GRID = [
    "..##.......",
    "#...#...#..",
    ".#....#..#.",
    "..#.#...#.#",
    ".#...##..#.",
    "..#.##.....",
    ".#.#.#....#",
    ".#........#",
    "#.##...#...",
    "#...##....#",
    ".#..#...#.#",
]


def test_part1():
    """Verify Part 1: slope right-3 down-1 hits 7 trees."""
    trees = count_trees(EXAMPLE_GRID, right=3, down=1)
    assert trees == 7, f"Expected 7, got {trees}"
    print(f"PASS  Part 1: {trees} trees")


def test_part2():
    """Verify Part 2: product of all five slopes is 336."""
    import math

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    counts = [count_trees(EXAMPLE_GRID, r, d) for r, d in slopes]
    product = math.prod(counts)
    assert counts == [2, 7, 3, 4, 2], f"Expected [2,7,3,4,2], got {counts}"
    assert product == 336, f"Expected 336, got {product}"
    print(f"PASS  Part 2: counts={counts}, product={product}")


if __name__ == "__main__":
    test_part1()
    test_part2()
    print("\nAll Day 3 tests passed!")
