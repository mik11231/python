#!/usr/bin/env python3
"""Advent of Code 2024 Day 19 Part 1 - Linen Layout.

Given a set of towel patterns and a list of designs, count how many
designs can be composed from the available patterns. Uses memoized
DP: dp[i] = whether design[i:] can be formed.
"""
from pathlib import Path
from functools import lru_cache


def solve(s: str) -> int:
    """Return the number of designs that are possible."""
    parts = s.strip().split("\n\n")
    patterns = tuple(p.strip() for p in parts[0].split(","))
    designs = parts[1].splitlines()

    def can_make(design):
        n = len(design)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(n):
            if not dp[i]:
                continue
            for p in patterns:
                if design[i:i + len(p)] == p:
                    dp[i + len(p)] = True
        return dp[n]

    return sum(1 for d in designs if can_make(d))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d19_input.txt").read_text()))
