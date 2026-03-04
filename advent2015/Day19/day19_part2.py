#!/usr/bin/env python3
"""Advent of Code 2015 Day 19 Part 2 — Fewest steps from e to molecule.

Reverse replacements and reduce molecule toward e; BFS or greedy rightmost-longest.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def parse(s: str) -> tuple[list[tuple[str, str]], str]:
    """Return (list of (from, to) for forward rules), molecule."""
    rules: list[tuple[str, str]] = []
    molecule = ""
    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue
        if " => " in line:
            a, b = line.split(" => ", 1)
            rules.append((a.strip(), b.strip()))
        else:
            molecule = line
    return rules, molecule


def solve(s: str) -> int:
    """Return fewest steps to produce molecule from e (reverse: reduce to e)."""
    rules, target = parse(s)
    # Reverse: replace B with A (to reduce)
    reverse = [(to, fr) for fr, to in rules]
    # Sort by length of replacement (longest first) for rightmost-longest
    reverse.sort(key=lambda p: -len(p[0]))
    steps = 0
    current = target
    while current != "e":
        changed = False
        for rhs, lhs in reverse:
            pos = current.rfind(rhs)  # rightmost
            if pos != -1:
                current = current[:pos] + lhs + current[pos + len(rhs) :]
                steps += 1
                changed = True
                break
        if not changed:
            raise RuntimeError("Greedy could not reduce to e")
    return steps


if __name__ == "__main__":
    text = Path(__file__).with_name("d19_input.txt").read_text(encoding="utf-8")
    print(solve(text))
