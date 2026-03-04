#!/usr/bin/env python3
"""Advent of Code 2017 Day 10 Part 1."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from knot import sparse_round


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
    lengths = [int(x) for x in s.strip().split(",") if x]
    a = list(range(256))
    sparse_round(a, lengths, 0, 0)
    return a[0] * a[1]


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d10_input.txt").read_text(encoding="utf-8")))
