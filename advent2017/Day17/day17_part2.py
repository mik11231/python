#!/usr/bin/env python3
"""Advent of Code 2017 Day 17 Part 2."""

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
    step = int(s.strip())
    pos = 0
    ans = -1
    size = 1
    for v in range(1, 50_000_001):
        pos = (pos + step) % size + 1
        if pos == 1:
            ans = v
        size += 1
    return ans


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d17_input.txt").read_text(encoding="utf-8")))
