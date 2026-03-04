#!/usr/bin/env python3
"""Advent of Code 2017 Day 15 Part 2."""

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
    i = 0
    while i < 5_000_000:
        while True:
            a = (a * 16807) % MOD
            if (a & 3) == 0:
                break
        while True:
            b = (b * 48271) % MOD
            if (b & 7) == 0:
                break
        c += (a & 0xFFFF) == (b & 0xFFFF)
        i += 1
    return c


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d15_input.txt").read_text(encoding="utf-8")))
