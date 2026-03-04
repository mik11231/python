#!/usr/bin/env python3
"""Example smoke tests for Day 16."""

from day16 import solve as solve1
from day16_part2 import solve as solve2


def main() -> None:
    # Minimal example: one Sue that matches ticker exactly
    example = """Sue 1: children: 3, cars: 2, perfumes: 1"""
    assert solve1(example) == 1
    # Sue that doesn't match
    example2 = """Sue 1: children: 5
Sue 2: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, goldfish: 5, trees: 3, cars: 2, perfumes: 1"""
    assert solve1(example2) == 2
    # Part 2: cats/trees must be > ticker; pomeranians/goldfish must be < ticker
    example3 = """Sue 1: cats: 8, trees: 4, goldfish: 4, pomeranians: 2, children: 3, samoyeds: 2, akitas: 0, vizslas: 0, cars: 2, perfumes: 1"""
    assert solve2(example3) == 1
    print("Part 1 and Part 2 examples: OK")


if __name__ == "__main__":
    main()
