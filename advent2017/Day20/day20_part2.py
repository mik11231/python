#!/usr/bin/env python3
"""Advent of Code 2017 Day 20 Part 2."""

from collections import Counter
from pathlib import Path
import re


PAT = re.compile(r"-?\d+")


def solve(s: str) -> int:
    parts = []
    for ln in s.splitlines():
        x = list(map(int, PAT.findall(ln)))
        parts.append([x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], True])

    for _ in range(200):
        pos = []
        for p in parts:
            if not p[9]:
                pos.append(None)
                continue
            p[3] += p[6]
            p[4] += p[7]
            p[5] += p[8]
            p[0] += p[3]
            p[1] += p[4]
            p[2] += p[5]
            pos.append((p[0], p[1], p[2]))
        cnt = Counter(x for x in pos if x is not None)
        for i, p in enumerate(parts):
            if p[9] and cnt[pos[i]] > 1:
                p[9] = False
    return sum(1 for p in parts if p[9])


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d20_input.txt").read_text(encoding="utf-8")))
