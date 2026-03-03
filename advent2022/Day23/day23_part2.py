#!/usr/bin/env python3
"""Advent of Code 2022 Day 23 Part 2.

Same elf diffusion; return the first round number when no elf moves.
"""
from pathlib import Path
from day23 import parse, round_

def solve(s):
    """Parse elves and return round number when no elf moves."""
    e=parse(s); off=0; r=0
    while True:
        r+=1
        e,m=round_(e,off); off=(off+1)%4
        if not m: return r

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d23_input.txt').read_text()))
