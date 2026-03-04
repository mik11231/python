#!/usr/bin/env python3
"""Advent of Code 2015 Day 10 — Elves Look, Say.

Start with input digit string; 40 times replace by count+digit runs. Return length.
"""
from pathlib import Path


def look_and_say(s: str) -> str:
    """One iteration: replace each run of same digit by count + digit."""
    out: list[str] = []
    i = 0
    while i < len(s):
        c = s[i]
        n = 0
        while i < len(s) and s[i] == c:
            n += 1
            i += 1
        out.append(str(n))
        out.append(c)
    return "".join(out)


def solve(s: str) -> int:
    """Return length after 40 look-and-say iterations."""
    text = s.strip()
    for _ in range(40):
        text = look_and_say(text)
    return len(text)


if __name__ == "__main__":
    text = Path(__file__).with_name("d10_input.txt").read_text(encoding="utf-8")
    print(solve(text))
