#!/usr/bin/env python3
"""Advent of Code 2022 Day 11 Part 2.

Same monkey simulation but 10000 rounds without worry division; use product
of all divisors as modulo to keep values bounded while preserving divisibility.
"""
from pathlib import Path
from day11 import parse, run

def solve(s):
    """Solve Part 2: 10000 rounds without relief, return monkey business."""
    return run(parse(s),10000,False)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d11_input.txt').read_text()))
