#!/usr/bin/env python3
"""Advent of Code 2017 Day 13 Part 1."""

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
    sev = 0
    for ln in s.splitlines():
        d, r = map(int, ln.split(": "))
        cyc = 2 * (r - 1)
        if d % cyc == 0:
            sev += d * r
    return sev


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d13_input.txt").read_text(encoding="utf-8")))
