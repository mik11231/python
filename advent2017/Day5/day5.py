#!/usr/bin/env python3
"""Advent of Code 2017 Day 5 Part 1."""

from pathlib import Path


def solve(s: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    a = [int(x) for x in s.split()]
    i = 0
    steps = 0
    n = len(a)
    while 0 <= i < n:
        j = a[i]
        a[i] += 1
        i += j
        steps += 1
    return steps


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d5_input.txt").read_text(encoding="utf-8")))
