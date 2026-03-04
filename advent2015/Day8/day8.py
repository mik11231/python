#!/usr/bin/env python3
"""Advent of Code 2015 Day 8 — Matchsticks.

Difference between string literal length and in-memory length (decode escapes).
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines


def solve(s: str) -> int:
    """Return sum of (literal length - in-memory length) per line."""
    total = 0
    for line in lines(s):
        line = line.strip()
        if not line:
            continue
        literal = len(line)
        # In-memory: strip surrounding "", decode \\ \" \xHH
        inner = line[1:-1]
        mem = 0
        i = 0
        while i < len(inner):
            if inner[i] == "\\":
                if i + 1 < len(inner) and inner[i + 1] in ('"', "\\"):
                    mem += 1
                    i += 2
                    continue
                if i + 1 < len(inner) and inner[i + 1] == "x" and i + 4 <= len(inner):
                    mem += 1
                    i += 4
                    continue
            mem += 1
            i += 1
        total += literal - mem
    return total


if __name__ == "__main__":
    text = Path(__file__).with_name("d8_input.txt").read_text(encoding="utf-8")
    print(solve(text))
