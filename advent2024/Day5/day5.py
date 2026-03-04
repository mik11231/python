#!/usr/bin/env python3
"""Advent of Code 2024 Day 5 Part 1 — Print Queue.

Given page ordering rules (X|Y means X before Y) and updates (lists of pages),
find which updates are already in the correct order and sum their middle pages.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Return sum of middle pages from correctly-ordered updates."""
    rules_s, updates_s = s.strip().split("\n\n")
    after = set()
    for line in rules_s.splitlines():
        a, b = line.split("|")
        after.add((int(a), int(b)))

    total = 0
    for line in updates_s.splitlines():
        pages = list(map(int, line.split(",")))
        valid = True
        for i in range(len(pages)):
            for j in range(i + 1, len(pages)):
                if (pages[j], pages[i]) in after:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            total += pages[len(pages) // 2]
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d5_input.txt").read_text()))
