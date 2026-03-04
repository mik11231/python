#!/usr/bin/env python3
"""Advent of Code 2017 Day 24 Part 2."""

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
    comps = [tuple(map(int, ln.split("/"))) for ln in s.splitlines() if ln.strip()]

    best_len = -1
    best_str = -1

    def dfs(port: int, used: int, length: int, strength: int) -> None:
        """
        Run `dfs` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: port, used, length, strength.
        - Returns the computed result for this stage of the pipeline.
        """
        nonlocal best_len, best_str
        if length > best_len or (length == best_len and strength > best_str):
            best_len = length
            best_str = strength
        for i, (a, b) in enumerate(comps):
            if (used >> i) & 1:
                continue
            if a == port or b == port:
                dfs(b if a == port else a, used | (1 << i), length + 1, strength + a + b)

    dfs(0, 0, 0, 0)
    return best_str


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d24_input.txt").read_text(encoding="utf-8")))
