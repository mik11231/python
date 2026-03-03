#!/usr/bin/env python3
"""Tests for Day 7 using the examples from the problem statement.

Example 1 (9 rules):
    Part 1 -> 4 bag colours can eventually contain shiny gold.
    Part 2 -> 32 individual bags inside shiny gold.

Example 2 (7 rules, deeply nested):
    Part 2 -> 126 individual bags inside shiny gold.
"""

from day7 import parse_rules, count_containers
from day7_part2 import count_bags_inside

EXAMPLE_1 = [
    "light red bags contain 1 bright white bag, 2 muted yellow bags.",
    "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
    "bright white bags contain 1 shiny gold bag.",
    "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
    "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
    "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
    "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
    "faded blue bags contain no other bags.",
    "dotted black bags contain no other bags.",
]

EXAMPLE_2 = [
    "shiny gold bags contain 2 dark red bags.",
    "dark red bags contain 2 dark orange bags.",
    "dark orange bags contain 2 dark yellow bags.",
    "dark yellow bags contain 2 dark green bags.",
    "dark green bags contain 2 dark blue bags.",
    "dark blue bags contain 2 dark violet bags.",
    "dark violet bags contain no other bags.",
]


def test_part1():
    """Verify Part 1: 4 bag colours can eventually contain shiny gold."""
    rules = parse_rules(EXAMPLE_1)
    result = count_containers(rules)
    assert result == 4, f"Expected 4 colours, got {result}"
    print(f"PASS  Part 1: {result} bag colours can contain shiny gold")


def test_part2_example1():
    """Verify Part 2 (example 1): 32 bags inside shiny gold."""
    rules = parse_rules(EXAMPLE_1)
    result = count_bags_inside(rules)
    assert result == 32, f"Expected 32 bags, got {result}"
    print(f"PASS  Part 2 (example 1): {result} bags inside shiny gold")


def test_part2_example2():
    """Verify Part 2 (example 2): 126 bags inside shiny gold."""
    rules = parse_rules(EXAMPLE_2)
    result = count_bags_inside(rules)
    assert result == 126, f"Expected 126 bags, got {result}"
    print(f"PASS  Part 2 (example 2): {result} bags inside shiny gold")


if __name__ == "__main__":
    test_part1()
    test_part2_example1()
    test_part2_example2()
    print("\nAll Day 7 tests passed!")
