#!/usr/bin/env python3
"""Advent of Code 2017 Day 21 Part 1."""

from pathlib import Path


def rots(grid: tuple[str, ...]) -> list[tuple[str, ...]]:
    """
    Run `rots` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid.
    - Returns the computed result for this stage of the pipeline.
    """
    out = []
    g = grid
    for _ in range(4):
        out.append(g)
        n = len(g)
        g = tuple("".join(g[n - 1 - c][r] for c in range(n)) for r in range(n))
    return out


def flips(grid: tuple[str, ...]) -> list[tuple[str, ...]]:
    """
    Run `flips` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid.
    - Returns the computed result for this stage of the pipeline.
    """
    return [grid, tuple(r[::-1] for r in grid)]


def parse(s: str) -> dict[tuple[str, ...], tuple[str, ...]]:
    """
    Run `parse` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    m = {}
    for ln in s.splitlines():
        a, b = ln.split(" => ")
        src = tuple(a.split("/"))
        dst = tuple(b.split("/"))
        for f in flips(src):
            for r in rots(f):
                m[r] = dst
    return m


def enhance(grid: tuple[str, ...], rules: dict[tuple[str, ...], tuple[str, ...]]) -> tuple[str, ...]:
    """
    Run `enhance` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid, rules.
    - Returns the computed result for this stage of the pipeline.
    """
    n = len(grid)
    k = 2 if n % 2 == 0 else 3
    blocks = n // k
    out_block = k + 1
    out = ["" for _ in range(blocks * out_block)]
    for br in range(blocks):
        for bc in range(blocks):
            src = tuple(grid[br * k + i][bc * k : bc * k + k] for i in range(k))
            dst = rules[src]
            for i in range(out_block):
                out[br * out_block + i] += dst[i]
    return tuple(out)


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
    rules = parse(s)
    g = (".#.", "..#", "###")
    for _ in range(5):
        g = enhance(g, rules)
    return sum(r.count("#") for r in g)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d21_input.txt").read_text(encoding="utf-8")))
