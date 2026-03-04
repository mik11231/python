#!/usr/bin/env python3
"""Advent of Code 2024 Day 2 Part 2 — Red-Nosed Reports (Problem Dampener).

Same rules as Part 1, but a report is also safe if removing any single level
makes the remaining sequence safe. Brute-force each removal.
"""
from pathlib import Path


def is_safe(levels: list[int]) -> bool:
    """
    Run `is_safe` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: levels.
    - Returns the computed result for this stage of the pipeline.
    """
    diffs = [b - a for a, b in zip(levels, levels[1:])]
    return all(1 <= d <= 3 for d in diffs) or all(-3 <= d <= -1 for d in diffs)


def is_safe_dampened(levels: list[int]) -> bool:
    """
    Run `is_safe_dampened` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: levels.
    - Returns the computed result for this stage of the pipeline.
    """
    if is_safe(levels):
        return True
    return any(is_safe(levels[:i] + levels[i + 1:]) for i in range(len(levels)))


def solve(s: str) -> int:
    """Return the number of safe reports with the Problem Dampener."""
    return sum(
        is_safe_dampened(list(map(int, line.split())))
        for line in s.strip().splitlines()
    )


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d2_input.txt").read_text()))
