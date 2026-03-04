#!/usr/bin/env python3
"""Advent of Code 2017 Day 12 Part 1."""

from collections import deque
from pathlib import Path


def parse(s: str) -> dict[int, list[int]]:
    """
    Run `parse` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    g = {}
    for ln in s.splitlines():
        a, b = ln.split(" <-> ")
        g[int(a)] = [int(x) for x in b.split(", ")]
    return g


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
    g = parse(s)
    q = deque([0])
    seen = {0}
    while q:
        u = q.popleft()
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d12_input.txt").read_text(encoding="utf-8")))
