#!/usr/bin/env python3
"""
advent2017/extras/python/days/day21.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2017.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

from __future__ import annotations

import argparse
import hashlib
import time
from functools import lru_cache
from pathlib import Path

EXPECTED_SHA = "759a25acf919be68478e4d20d3856f488ff79325d0954d8ca5c89cecc2fd8287"
EXPECTED_PART1 = "139"
EXPECTED_PART2 = "1857134"


def resolve_input(provided: str | None) -> Path:
    """
    Run `resolve_input` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: provided.
    - Returns the computed result for this stage of the pipeline.
    """
    if provided:
        return Path(provided).resolve()
    for c in (
        "advent2017/Day21/d21_input.txt",
        "Day21/d21_input.txt",
        "../Day21/d21_input.txt",
        "../../Day21/d21_input.txt",
    ):
        p = Path(c)
        if p.exists():
            return p.resolve()
    raise SystemExit("input not found")


def sha256_file(path: Path) -> str:
    """
    Run `sha256_file` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rotate(p: tuple[str, ...]) -> tuple[str, ...]:
    """
    Run `rotate` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: p.
    - Returns the computed result for this stage of the pipeline.
    """
    n = len(p)
    return tuple("".join(p[n - 1 - r][c] for r in range(n)) for c in range(n))


def flip(p: tuple[str, ...]) -> tuple[str, ...]:
    """
    Run `flip` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: p.
    - Returns the computed result for this stage of the pipeline.
    """
    return tuple(row[::-1] for row in p)


def canonical(p: tuple[str, ...]) -> tuple[str, ...]:
    """
    Run `canonical` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: p.
    - Returns the computed result for this stage of the pipeline.
    """
    cur = p
    vars_: list[tuple[str, ...]] = []
    for _ in range(4):
        vars_.append(cur)
        vars_.append(flip(cur))
        cur = rotate(cur)
    return min(vars_)


def parse_rules(text: str) -> dict[tuple[str, ...], tuple[str, ...]]:
    """
    Run `parse_rules` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: text.
    - Returns the computed result for this stage of the pipeline.
    """
    rules: dict[tuple[str, ...], tuple[str, ...]] = {}
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        left, right = s.split(" => ")
        inp = tuple(left.split("/"))
        out = tuple(right.split("/"))
        rules[canonical(inp)] = out
    return rules


def split_blocks(grid: tuple[str, ...], bs: int) -> list[tuple[str, ...]]:
    """
    Run `split_blocks` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid, bs.
    - Returns the computed result for this stage of the pipeline.
    """
    n = len(grid)
    cnt = n // bs
    out: list[tuple[str, ...]] = []
    for br in range(cnt):
        for bc in range(cnt):
            out.append(tuple(grid[br * bs + r][bc * bs : bc * bs + bs] for r in range(bs)))
    return out


def run_iters(rules: dict[tuple[str, ...], tuple[str, ...]], n: int) -> int:
    """
    Run `run_iters` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: rules, n.
    - Returns the computed result for this stage of the pipeline.
    """
    def enhance_once(grid: tuple[str, ...]) -> tuple[str, ...]:
        """
        Run `enhance_once` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: grid.
        - Returns the computed result for this stage of the pipeline.
        """
        size = len(grid)
        bs = 2 if size % 2 == 0 else 3
        os = bs + 1
        cnt = size // bs
        out = [["."] * (cnt * os) for _ in range(cnt * os)]
        for br in range(cnt):
            for bc in range(cnt):
                sub = tuple(grid[br * bs + r][bc * bs : bc * bs + bs] for r in range(bs))
                rep = rules[canonical(sub)]
                for r in range(os):
                    for c in range(os):
                        out[br * os + r][bc * os + c] = rep[r][c]
        return tuple("".join(row) for row in out)

    def popcount(p: tuple[str, ...]) -> int:
        """
        Run `popcount` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: p.
        - Returns the computed result for this stage of the pipeline.
        """
        return sum(row.count("#") for row in p)

    init = (".#.", "..#", "###")
    if n <= 5:
        g = init
        for _ in range(n):
            g = enhance_once(g)
        return popcount(g)

    @lru_cache(maxsize=None)
    def expand_three_steps_from_3(p: tuple[str, ...]) -> tuple[tuple[str, ...], ...]:
        """
        Run `expand_three_steps_from_3` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: p.
        - Returns the computed result for this stage of the pipeline.
        """
        g = enhance_once(enhance_once(enhance_once(p)))
        return tuple(split_blocks(g, 3))

    @lru_cache(maxsize=None)
    def count_after_cycles(p: tuple[str, ...], cycles: int) -> int:
        """
        Run `count_after_cycles` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: p, cycles.
        - Returns the computed result for this stage of the pipeline.
        """
        if cycles == 0:
            return popcount(p)
        return sum(count_after_cycles(sub, cycles - 1) for sub in expand_three_steps_from_3(p))

    if n % 3 == 0:
        return count_after_cycles(init, n // 3)
    g = init
    for _ in range(n):
        g = enhance_once(g)
    return popcount(g)


def main() -> int:
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, choices=[1, 2], required=True)
    ap.add_argument("--input")
    args = ap.parse_args()

    in_path = resolve_input(args.input)
    if sha256_file(in_path) != EXPECTED_SHA:
        raise SystemExit("checksum mismatch")
    rules = parse_rules(in_path.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    ans = str(run_iters(rules, 5 if args.part == 1 else 18))
    ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if ans != expected:
        raise SystemExit(f"answer mismatch: got {ans}, expected {expected}")
    print(ans)
    print(f"[python-fancy] day=21 part={args.part} runtime_ms={ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
