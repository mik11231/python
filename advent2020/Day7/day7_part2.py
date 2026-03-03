#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 7: Handy Haversacks (Part 2)

How many individual bags are required inside a single shiny gold bag?

Algorithm
---------
Recursive (memoised) counting.  For a given bag colour, the total number of
bags inside it is the sum over each child of:

    child_count * (1 + bags_inside(child_colour))

where the 1 accounts for the child bag itself, and `bags_inside` recurses
into whatever *that* child must contain.  A bag that contains "no other bags"
returns 0.
"""

from functools import lru_cache
from pathlib import Path

from day7 import parse_rules


def count_bags_inside(rules: dict[str, list[tuple[int, str]]], target: str = "shiny gold") -> int:
    """Return the total number of individual bags required inside *target*."""

    @lru_cache(maxsize=None)
    def _inner(colour: str) -> int:
        return sum(
            count * (1 + _inner(child))
            for count, child in rules.get(colour, [])
        )

    return _inner(target)


def solve(input_path: str = "advent2020/Day7/d7_input.txt") -> int:
    """Read the bag rules and count bags inside shiny gold."""
    lines = Path(input_path).read_text().splitlines()
    rules = parse_rules(lines)
    return count_bags_inside(rules)


if __name__ == "__main__":
    result = solve()
    print(f"Individual bags inside shiny gold: {result}")
