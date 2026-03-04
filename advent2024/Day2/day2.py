#!/usr/bin/env python3
"""Advent of Code 2024 Day 2 Part 1 — Red-Nosed Reports.

A report (line of numbers) is safe if its levels are all increasing or all
decreasing and every adjacent pair differs by 1..3. Count the safe reports.
"""
from pathlib import Path


def is_safe(levels: list[int]) -> bool:
    diffs = [b - a for a, b in zip(levels, levels[1:])]
    return all(1 <= d <= 3 for d in diffs) or all(-3 <= d <= -1 for d in diffs)


def solve(s: str) -> int:
    """Return the number of safe reports."""
    return sum(
        is_safe(list(map(int, line.split())))
        for line in s.strip().splitlines()
    )


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d2_input.txt").read_text()))
