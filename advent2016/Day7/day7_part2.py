#!/usr/bin/env python3
"""Advent of Code 2016 Day 7 Part 2: SSL support."""

from pathlib import Path
import re


def abas(t: str) -> set[tuple[str, str]]:
    """Return all (a,b) pairs representing ABA patterns a b a."""
    out: set[tuple[str, str]] = set()
    for i in range(len(t) - 2):
        a, b, c = t[i : i + 3]
        if a == c and a != b:
            out.add((a, b))
    return out


def solve(s: str) -> int:
    """Count IPs supporting SSL."""
    total = 0
    for line in s.splitlines():
        parts = re.split(r"\[|\]", line.strip())
        outs = parts[0::2]
        ins = parts[1::2]
        need = set()
        for t in outs:
            for a, b in abas(t):
                need.add((b, a))  # BAB expected inside
        inside = set()
        for t in ins:
            inside |= abas(t)
        if need & inside:
            total += 1
    return total


if __name__ == "__main__":
    text = Path(__file__).with_name("d7_input.txt").read_text(encoding="utf-8")
    print(solve(text))
