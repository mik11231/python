#!/usr/bin/env python3
"""Advent of Code 2024 Day 19 Part 2 - Linen Layout (count all ways).

For each design, count all distinct ways to compose it from the
available patterns using DP: dp[i] = number of ways to form design[i:].
Sum the counts over all designs.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Return the total number of ways to make all possible designs."""
    parts = s.strip().split("\n\n")
    patterns = tuple(p.strip() for p in parts[0].split(","))
    designs = parts[1].splitlines()

    def count_ways(design):
        """
        Run `count_ways` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: design.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        n = len(design)
        dp = [0] * (n + 1)
        dp[0] = 1
        for i in range(n):
            if dp[i] == 0:
                continue
            for p in patterns:
                if design[i:i + len(p)] == p:
                    dp[i + len(p)] += dp[i]
        return dp[n]

    return sum(count_ways(d) for d in designs)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d19_input.txt").read_text()))
