#!/usr/bin/env python3
"""Advent of Code 2017 Day 6 Part 2."""

from pathlib import Path


def redistribute(a: list[int]) -> None:
    i = max(range(len(a)), key=lambda k: (a[k], -k))
    v = a[i]
    a[i] = 0
    n = len(a)
    q, r = divmod(v, n)
    if q:
        for k in range(n):
            a[k] += q
    for t in range(1, r + 1):
        a[(i + t) % n] += 1


def solve(s: str) -> int:
    a = list(map(int, s.split()))
    seen = {}
    steps = 0
    while tuple(a) not in seen:
        seen[tuple(a)] = steps
        redistribute(a)
        steps += 1
    return steps - seen[tuple(a)]


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d6_input.txt").read_text(encoding="utf-8")))
