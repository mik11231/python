#!/usr/bin/env python3
"""Advent of Code 2024 Day 5 Part 2 — Print Queue (fix invalid updates).

For incorrectly-ordered updates, sort them using the ordering rules as a
comparator, then sum the middle pages. Uses functools.cmp_to_key for sorting.
"""
from functools import cmp_to_key
from pathlib import Path


def solve(s: str) -> int:
    """Return sum of middle pages from fixed incorrectly-ordered updates."""
    rules_s, updates_s = s.strip().split("\n\n")
    after = set()
    for line in rules_s.splitlines():
        a, b = line.split("|")
        after.add((int(a), int(b)))

    def cmp(a: int, b: int) -> int:
        """
        Run `cmp` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: a, b.
        - Returns the computed result for this stage of the pipeline.
        """
        if (a, b) in after:
            return -1
        if (b, a) in after:
            return 1
        return 0

    total = 0
    for line in updates_s.splitlines():
        pages = list(map(int, line.split(",")))
        sorted_pages = sorted(pages, key=cmp_to_key(cmp))
        if sorted_pages != pages:
            total += sorted_pages[len(sorted_pages) // 2]
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d5_input.txt").read_text()))
