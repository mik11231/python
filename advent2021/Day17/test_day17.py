#!/usr/bin/env python3
"""Tests for Day 17: Trick Shot."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from day17 import parse_target
from day17_part2 import count_valid_velocities

EXAMPLE = "target area: x=20..30, y=-10..-5"


def test_part1_example():
    """Maximum y position for x=20..30, y=-10..-5 is 45."""
    _, _, y1, y2 = parse_target(EXAMPLE)
    y_min = min(y1, y2)
    vy = abs(y_min) - 1
    assert vy * (vy + 1) // 2 == 45


def test_part2_example():
    """112 distinct initial velocities hit x=20..30, y=-10..-5."""
    x1, x2, y1, y2 = parse_target(EXAMPLE)
    assert count_valid_velocities(x1, x2, y1, y2) == 112
