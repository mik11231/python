#!/usr/bin/env python3
"""Advent of Code 2017 Day 23 Part 1."""

from collections import defaultdict
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
    p = [ln.split() for ln in s.splitlines() if ln.strip()]
    r = defaultdict(int)

    def val(x: str) -> int:
        """
        Run `val` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: x.
        - Returns the computed result for this stage of the pipeline.
        """
        return int(x) if x.lstrip("-").isdigit() else r[x]

    i = 0
    muls = 0
    while 0 <= i < len(p):
        op, x, y = p[i]
        if op == "set":
            r[x] = val(y)
        elif op == "sub":
            r[x] -= val(y)
        elif op == "mul":
            r[x] *= val(y)
            muls += 1
        elif op == "jnz":
            if val(x) != 0:
                i += val(y)
                continue
        i += 1
    return muls


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d23_input.txt").read_text(encoding="utf-8")))
