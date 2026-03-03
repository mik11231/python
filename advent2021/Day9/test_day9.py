#!/usr/bin/env python3
"""Tests for Day 9: Smoke Basin."""

from math import prod

from day9 import parse_grid, find_low_points
from day9_part2 import basin_sizes

EXAMPLE = """\
2199943210
3987894921
9856789892
8767896789
9899965678"""


def test_low_point_heights():
    """The example heightmap has 4 low points with heights 1, 0, 5, 5."""
    grid = parse_grid(EXAMPLE)
    heights = sorted(h for _, _, h in find_low_points(grid))
    assert heights == [0, 1, 5, 5]


def test_risk_level_sum():
    """Sum of risk levels (height + 1) for the example is 15."""
    grid = parse_grid(EXAMPLE)
    assert sum(h + 1 for _, _, h in find_low_points(grid)) == 15


def test_basin_product():
    """Three largest basins have sizes 14, 9, 9; product is 1134."""
    grid = parse_grid(EXAMPLE)
    sizes = sorted(basin_sizes(grid), reverse=True)
    assert prod(sizes[:3]) == 1134
