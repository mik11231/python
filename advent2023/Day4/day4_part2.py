#!/usr/bin/env python3
"""Advent of Code 2023 Day 4 Part 2 — Scratchcards.

Instead of points, each match on card i wins one copy each of cards
i+1, i+2, ..., i+matches. Process all originals and copies. Return
the total number of scratchcards you end up with.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    lines = s.strip().splitlines()
    counts = [1] * len(lines)
    for i, line in enumerate(lines):
        _, numbers = line.split(": ")
        winning, have = numbers.split(" | ")
        win_set = set(winning.split())
        matches = sum(1 for n in have.split() if n in win_set)
        for j in range(i + 1, min(i + 1 + matches, len(lines))):
            counts[j] += counts[i]
    return sum(counts)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d4_input.txt").read_text()))
