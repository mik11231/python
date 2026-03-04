#!/usr/bin/env python3
"""Advent of Code 2017 Day 7 Part 1."""

from pathlib import Path


def solve(s: str) -> str:
    all_nodes = set()
    children = set()
    for line in s.splitlines():
        left, *right = line.split("->")
        name = left.split()[0]
        all_nodes.add(name)
        if right:
            for c in right[0].split(","):
                children.add(c.strip())
    return next(iter(all_nodes - children))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d7_input.txt").read_text(encoding="utf-8")))
