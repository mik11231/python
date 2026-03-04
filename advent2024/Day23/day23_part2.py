#!/usr/bin/env python3
"""Advent of Code 2024 Day 23 Part 2 - LAN Party (largest clique).

Find the largest clique using Bron-Kerbosch with pivoting, then return
the node names sorted and joined with commas.
"""
from pathlib import Path
from collections import defaultdict


def solve(s: str) -> str:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    adj = defaultdict(set)
    for line in s.strip().splitlines():
        a, b = line.split('-')
        adj[a].add(b)
        adj[b].add(a)

    best = []

    def bron_kerbosch(r, p, x):
        """
        Run `bron_kerbosch` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: r, p, x.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        nonlocal best
        if not p and not x:
            if len(r) > len(best):
                best = list(r)
            return
        pivot = max(p | x, key=lambda v: len(adj[v] & p))
        for v in p - adj[pivot]:
            bron_kerbosch(r | {v}, p & adj[v], x & adj[v])
            p = p - {v}
            x = x | {v}

    bron_kerbosch(set(), set(adj.keys()), set())
    return ','.join(sorted(best))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d23_input.txt").read_text()))
