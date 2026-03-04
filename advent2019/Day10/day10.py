"""Advent of Code 2019 Day 10 Part 1."""

from math import gcd
from pathlib import Path


def parse(s: str):
    """
    Run `parse` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    pts = []
    for y, row in enumerate(s.splitlines()):
        for x, ch in enumerate(row.strip()):
            if ch == '#':
                pts.append((x, y))
    return pts


def visible_from(a, pts):
    """
    Run `visible_from` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: a, pts.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    ax, ay = a
    dirs = set()
    for bx, by in pts:
        if (bx, by) == a:
            continue
        dx, dy = bx - ax, by - ay
        g = gcd(abs(dx), abs(dy))
        dirs.add((dx // g, dy // g))
    return len(dirs)


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
    pts = parse(s)
    return max(visible_from(p, pts) for p in pts)


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d10_input.txt').read_text()))
