#!/usr/bin/env python3
"""Tests for Day 13: Transparent Origami."""

from day13 import parse_input, fold
from day13_part2 import render

EXAMPLE = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


def test_first_fold():
    """After the first fold (y=7), 17 dots remain visible."""
    dots, folds = parse_input(EXAMPLE)
    dots = fold(dots, folds[0])
    assert len(dots) == 17


def test_all_folds_render():
    """After all folds the example produces a 5×5 square outline."""
    dots, folds = parse_input(EXAMPLE)
    for instruction in folds:
        dots = fold(dots, instruction)
    expected = (
        "#####\n"
        "#...#\n"
        "#...#\n"
        "#...#\n"
        "#####"
    )
    assert render(dots) == expected
