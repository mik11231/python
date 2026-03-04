#!/usr/bin/env python3
"""Advent of Code 2017 Day 12 Part 2."""

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
    rem = set(g)
    groups = 0
    while rem:
        groups += 1
        src = next(iter(rem))
        q = deque([src])
        rem.remove(src)
        while q:
            u = q.popleft()
            for v in g[u]:
                if v in rem:
                    rem.remove(v)
                    q.append(v)
    return groups


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d12_input.txt").read_text(encoding="utf-8")))
