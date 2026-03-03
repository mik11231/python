#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 14: Extended Polymerization (Part 2)

Same pair-insertion polymerization, but now run for 40 steps instead of 10.
The pair-counting approach from Part 1 handles this efficiently because the
number of *distinct* pairs is bounded by the alphabet size squared, regardless
of the exponentially growing polymer length.
"""

from collections import Counter
from pathlib import Path

from day14 import parse_input, polymerize, element_counts


def solve(input_path: str = "advent2021/Day14/d14_input.txt") -> int:
    """Read puzzle input, run 40 polymerization steps, and return
    most_common - least_common element count."""
    text = Path(input_path).read_text()
    template, rules = parse_input(text)
    pair_counts: Counter = Counter()
    for i in range(len(template) - 1):
        pair_counts[template[i] + template[i + 1]] += 1
    pair_counts = polymerize(pair_counts, rules, 40)
    counts = element_counts(pair_counts, template[0], template[-1])
    ordered = counts.most_common()
    return ordered[0][1] - ordered[-1][1]


if __name__ == "__main__":
    result = solve()
    print(f"Most common minus least common after 40 steps: {result}")
