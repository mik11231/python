#!/usr/bin/env python3
"""Advent of Code 2022 Day 9 Part 2.

Same rope simulation as Part 1 but with 10 knots; count distinct positions
visited by the final tail segment.
"""
from pathlib import Path
from day9 import sim

def solve(s:str)->int:
    """Solve Part 2: count tail positions for a 10-knot rope."""
    return sim(s,10)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d9_input.txt').read_text()))
