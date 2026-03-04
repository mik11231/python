#!/usr/bin/env python3
"""Advent of Code 2017 Day 9 Part 1."""

from pathlib import Path


def solve(s: str) -> int:
    t = s.strip()
    depth = 0
    score = 0
    garb = False
    i = 0
    while i < len(t):
        c = t[i]
        if garb:
            if c == "!":
                i += 2
                continue
            if c == ">":
                garb = False
        else:
            if c == "<":
                garb = True
            elif c == "{":
                depth += 1
                score += depth
            elif c == "}":
                depth -= 1
        i += 1
    return score


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d9_input.txt").read_text(encoding="utf-8")))
