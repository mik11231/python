#!/usr/bin/env python3
"""Tests for Day 12: Passage Pathing."""

from day12 import parse_graph, count_paths
from day12_part2 import count_paths_part2

SMALL_EXAMPLE = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

MEDIUM_EXAMPLE = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""


def test_small_part1():
    """The small example has 10 paths with single-visit small caves."""
    graph = parse_graph(SMALL_EXAMPLE)
    assert count_paths(graph) == 10


def test_small_part2():
    """The small example has 36 paths when one double-visit is allowed."""
    graph = parse_graph(SMALL_EXAMPLE)
    assert count_paths_part2(graph) == 36


def test_medium_part1():
    """The medium example has 19 paths."""
    graph = parse_graph(MEDIUM_EXAMPLE)
    assert count_paths(graph) == 19


def test_medium_part2():
    """The medium example has 103 paths with one double-visit."""
    graph = parse_graph(MEDIUM_EXAMPLE)
    assert count_paths_part2(graph) == 103
