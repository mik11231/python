#!/usr/bin/env python3
"""Advent of Code 2017 Day 19 Part 1."""

from pathlib import Path


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
    g = s.splitlines()
    w = max(len(r) for r in g)
    g = [r.ljust(w) for r in g]
    r = 0
    c = g[0].index("|")
    dr, dc = 1, 0
    out = []
    while True:
        ch = g[r][c]
        if ch == " ":
            break
        if ch.isalpha():
            out.append(ch)
        if ch == "+":
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if (nr, nc) == (r - dr, c - dc):
                    continue
                if 0 <= nr < len(g) and 0 <= nc < w and g[nr][nc] != " ":
                    dr, dc = nr - r, nc - c
                    break
        r += dr
        c += dc
    return "".join(out)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d19_input.txt").read_text(encoding="utf-8")))
