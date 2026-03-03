#!/usr/bin/env python3
"""Tests for Day 17: Conway Cubes using the puzzle example."""

from day17 import parse_initial_state, simulate

EXAMPLE = """\
.#.
..#
###
"""


def test_parse_initial_state_3d() -> None:
    """Verify 3D parsing yields 5 active cubes at correct coordinates."""
    active = parse_initial_state(EXAMPLE, dimensions=3)
    assert len(active) == 5
    assert (1, 0, 0) in active
    assert (2, 1, 0) in active


def test_3d_six_cycles() -> None:
    """Verify Part 1: 112 active cubes after 6 cycles in 3D."""
    initial = parse_initial_state(EXAMPLE, dimensions=3)
    final = simulate(initial, dimensions=3, cycles=6)
    assert len(final) == 112


def test_4d_six_cycles() -> None:
    """Verify Part 2: 848 active cubes after 6 cycles in 4D."""
    initial = parse_initial_state(EXAMPLE, dimensions=4)
    final = simulate(initial, dimensions=4, cycles=6)
    assert len(final) == 848


if __name__ == "__main__":
    test_parse_initial_state_3d()
    test_3d_six_cycles()
    test_4d_six_cycles()
    print("All Day 17 tests passed!")
