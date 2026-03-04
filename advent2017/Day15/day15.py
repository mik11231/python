#!/usr/bin/env python3
"""Advent of Code 2017 Day 15 Part 1."""

from pathlib import Path


MOD = 2147483647


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
    a, b = [int(ln.split()[-1]) for ln in s.splitlines() if ln.strip()]
    c = 0
    for _ in range(40_000_000):
        a = (a * 16807) % MOD
        b = (b * 48271) % MOD
        c += (a & 0xFFFF) == (b & 0xFFFF)
    return c


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d15_input.txt").read_text(encoding="utf-8")))
