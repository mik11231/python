#!/usr/bin/env python3
"""Advent of Code 2017 Day 7 Part 2."""

from collections import Counter
from functools import lru_cache
from pathlib import Path


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
    w = {}
    ch = {}
    parent = {}
    for line in s.splitlines():
        left, *right = line.split("->")
        p = left.split()[0]
        wt = int(left.split()[1][1:-1])
        w[p] = wt
        kids = []
        if right:
            kids = [x.strip() for x in right[0].split(",")]
            for c in kids:
                parent[c] = p
        ch[p] = kids

    root = next(x for x in w if x not in parent)

    @lru_cache(maxsize=None)
    def total(n: str) -> int:
        """
        Run `total` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: n.
        - Returns the computed result for this stage of the pipeline.
        """
        return w[n] + sum(total(c) for c in ch[n])

    def dfs(n: str) -> int | None:
        """
        Run `dfs` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: n.
        - Returns the computed result for this stage of the pipeline.
        """
        ts = [total(c) for c in ch[n]]
        if len(set(ts)) <= 1:
            return None
        cnt = Counter(ts)
        bad_total = next(k for k, v in cnt.items() if v == 1)
        good_total = next(k for k, v in cnt.items() if v > 1)
        bad_child = ch[n][ts.index(bad_total)]
        deeper = dfs(bad_child)
        if deeper is not None:
            return deeper
        return w[bad_child] + (good_total - bad_total)

    ans = dfs(root)
    if ans is None:
        raise ValueError("no imbalance")
    return ans


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d7_input.txt").read_text(encoding="utf-8")))
