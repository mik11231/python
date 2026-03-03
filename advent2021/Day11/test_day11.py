#!/usr/bin/env python3
"""Tests for Day 11: Dumbo Octopus."""

from day11 import parse_grid, step

EXAMPLE = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


def test_flashes_after_100_steps():
    """After 100 steps the example grid produces 1656 total flashes."""
    grid = parse_grid(EXAMPLE)
    assert sum(step(grid) for _ in range(100)) == 1656


def test_first_synchronized_flash():
    """The first synchronised flash in the example occurs at step 195."""
    grid = parse_grid(EXAMPLE)
    total_cells = len(grid) * len(grid[0])
    step_num = 0
    while True:
        step_num += 1
        if step(grid) == total_cells:
            break
    assert step_num == 195
