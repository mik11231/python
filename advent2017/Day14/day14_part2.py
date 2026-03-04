#!/usr/bin/env python3
"""Advent of Code 2017 Day 14 Part 2."""

from collections import deque
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from knot import knot_hash


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
    key = s.strip()
    g = []
    for i in range(128):
        h = knot_hash(f"{key}-{i}")
        bits = "".join(f"{int(c,16):04b}" for c in h)
        g.append([ch == "1" for ch in bits])
    seen = [[False] * 128 for _ in range(128)]
    comp = 0
    for r in range(128):
        for c in range(128):
            if not g[r][c] or seen[r][c]:
                continue
            comp += 1
            q = deque([(r, c)])
            seen[r][c] = True
            while q:
                x, y = q.popleft()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < 128 and 0 <= ny < 128 and g[nx][ny] and not seen[nx][ny]:
                        seen[nx][ny] = True
                        q.append((nx, ny))
    return comp


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d14_input.txt").read_text(encoding="utf-8")))
