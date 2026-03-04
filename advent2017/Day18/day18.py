#!/usr/bin/env python3
"""Advent of Code 2017 Day 18 Part 1."""

from collections import defaultdict
from pathlib import Path


def solve(s: str) -> int:
    p = [ln.split() for ln in s.splitlines() if ln.strip()]
    r = defaultdict(int)

    def val(x: str) -> int:
        return int(x) if x.lstrip("-").isdigit() else r[x]

    i = 0
    snd = 0
    while 0 <= i < len(p):
        op, *a = p[i]
        if op == "snd":
            snd = val(a[0])
        elif op == "set":
            r[a[0]] = val(a[1])
        elif op == "add":
            r[a[0]] += val(a[1])
        elif op == "mul":
            r[a[0]] *= val(a[1])
        elif op == "mod":
            r[a[0]] %= val(a[1])
        elif op == "rcv":
            if val(a[0]) != 0:
                return snd
        elif op == "jgz":
            if val(a[0]) > 0:
                i += val(a[1])
                continue
        i += 1
    raise ValueError("no recover")


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d18_input.txt").read_text(encoding="utf-8")))
