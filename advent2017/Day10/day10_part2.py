#!/usr/bin/env python3
"""Advent of Code 2017 Day 10 Part 2."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from knot import knot_hash


def solve(s: str) -> str:
    return knot_hash(s.strip())


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d10_input.txt").read_text(encoding="utf-8")))
