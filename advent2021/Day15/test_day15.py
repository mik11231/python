#!/usr/bin/env python3
"""Tests for Day 15: Chiton."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from day15 import parse_grid, dijkstra
from day15_part2 import expand_grid

EXAMPLE = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""


def test_part1_example():
    """Lowest risk path in the 10x10 example grid is 40."""
    grid = parse_grid(EXAMPLE)
    assert dijkstra(grid) == 40


def test_part2_example():
    """Lowest risk path in the 5x-expanded example grid is 315."""
    grid = parse_grid(EXAMPLE)
    assert dijkstra(expand_grid(grid)) == 315
