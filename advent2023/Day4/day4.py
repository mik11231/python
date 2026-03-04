#!/usr/bin/env python3
"""Advent of Code 2023 Day 4 Part 1 — Scratchcards.

Each card has winning numbers and your numbers. The first match is worth
1 point, each subsequent match doubles the value. Return the total points.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    total = 0
    for line in s.strip().splitlines():
        _, numbers = line.split(": ")
        winning, have = numbers.split(" | ")
        win_set = set(winning.split())
        matches = sum(1 for n in have.split() if n in win_set)
        if matches:
            total += 1 << (matches - 1)
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d4_input.txt").read_text()))
