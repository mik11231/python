#!/usr/bin/env python3
"""Advent of Code 2016 Day 12 Part 1: Leonardo's Monorail."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assembunny import parse_program, run_program


def solve(s: str) -> int:
    """Run assembunny with c=0 and return register a."""
    program = parse_program(s)
    res = run_program(program, {"a": 0, "b": 0, "c": 0, "d": 0})
    return res.regs["a"]


if __name__ == "__main__":
    text = Path(__file__).with_name("d12_input.txt").read_text(encoding="utf-8")
    print(solve(text))
