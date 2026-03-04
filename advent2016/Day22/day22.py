#!/usr/bin/env python3
"""Advent of Code 2016 Day 22 Part 1: Grid Computing viable pairs."""

from pathlib import Path
import re


NODE_RE = re.compile(r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T")


def parse(s: str) -> list[tuple[int, int, int, int, int]]:
    """Parse node table as (x,y,size,used,avail)."""
    out = []
    for ln in s.splitlines():
        m = NODE_RE.search(ln)
        if m:
            out.append(tuple(map(int, m.groups())))
    return out


def solve(s: str) -> int:
    """Count viable pairs A!=B where A.used>0 and A.used<=B.avail."""
    nodes = parse(s)
    total = 0
    for i, a in enumerate(nodes):
        ua = a[3]
        if ua == 0:
            continue
        for j, b in enumerate(nodes):
            if i == j:
                continue
            if ua <= b[4]:
                total += 1
    return total


if __name__ == "__main__":
    text = Path(__file__).with_name("d22_input.txt").read_text(encoding="utf-8")
    print(solve(text))
