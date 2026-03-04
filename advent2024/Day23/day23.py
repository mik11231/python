#!/usr/bin/env python3
"""Advent of Code 2024 Day 23 Part 1 - LAN Party.

Build an adjacency set from the connection list. For every edge (a, b), find
all common neighbours c forming a triangle. Count triangles where at least
one node starts with 't'.
"""
from pathlib import Path
from collections import defaultdict


def solve(s: str) -> int:
    adj = defaultdict(set)
    for line in s.strip().splitlines():
        a, b = line.split('-')
        adj[a].add(b)
        adj[b].add(a)

    triangles = set()
    for a in adj:
        for b in adj[a]:
            for c in adj[a] & adj[b]:
                triangles.add(tuple(sorted((a, b, c))))

    return sum(1 for t in triangles if any(n.startswith('t') for n in t))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d23_input.txt").read_text()))
