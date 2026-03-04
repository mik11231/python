#!/usr/bin/env python3
"""Advent of Code 2024 Day 1 Part 2 — Historian Hysteria (Similarity Score).

For each number in the left list, multiply it by how many times it appears in
the right list. The answer is the sum of all such products.
"""
from collections import Counter
from pathlib import Path


def solve(s: str) -> int:
    """Return the similarity score between the two lists."""
    left, right = [], []
    for line in s.strip().splitlines():
        a, b = line.split()
        left.append(int(a))
        right.append(int(b))
    counts = Counter(right)
    return sum(n * counts[n] for n in left)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d1_input.txt").read_text()))
