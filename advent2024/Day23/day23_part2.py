#!/usr/bin/env python3
"""Advent of Code 2024 Day 23 Part 2 - LAN Party (largest clique).

Find the largest clique using Bron-Kerbosch with pivoting, then return
the node names sorted and joined with commas.
"""
from pathlib import Path
from collections import defaultdict


def solve(s: str) -> str:
    adj = defaultdict(set)
    for line in s.strip().splitlines():
        a, b = line.split('-')
        adj[a].add(b)
        adj[b].add(a)

    best = []

    def bron_kerbosch(r, p, x):
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
