#!/usr/bin/env python3
"""Advent of Code 2022 Day 10 Part 2.

Render the CRT screen: each pixel is lit if the sprite (3 pixels centered on
X) overlaps that position during the cycle. Returns 6 lines of 40 characters.
"""
from pathlib import Path
from day10 import ticks

def solve(s:str)->str:
    """Solve Part 2: render CRT output as 6 lines of # and . characters."""
    vals=list(ticks(s))
    out=[]
    for i,x in enumerate(vals[:240]):
        col=i%40
        out.append('#' if abs(col-x)<=1 else '.')
    return '\n'.join(''.join(out[r*40:(r+1)*40]) for r in range(6))

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d10_input.txt').read_text()))
