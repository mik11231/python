#!/usr/bin/env python3
"""Tests for Day 14: Extended Polymerization."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collections import Counter

from day14 import parse_input, polymerize, element_counts

EXAMPLE = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""


def _run(steps: int) -> int:
    """Helper: run the example for *steps* and return max - min count."""
    template, rules = parse_input(EXAMPLE)
    pair_counts: Counter = Counter()
    for i in range(len(template) - 1):
        pair_counts[template[i] + template[i + 1]] += 1
    pair_counts = polymerize(pair_counts, rules, steps)
    counts = element_counts(pair_counts, template[0], template[-1])
    ordered = counts.most_common()
    return ordered[0][1] - ordered[-1][1]


def test_part1_example():
    """After 10 steps: B=1749, H=161 -> answer 1588."""
    assert _run(10) == 1588


def test_part2_example():
    """After 40 steps: answer 2188189693529."""
    assert _run(40) == 2188189693529
