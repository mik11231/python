#!/usr/bin/env python3
"""Advent of Code 2022 Day 10 Part 1.

Cathode-Ray Tube: simulate CPU cycles and X register during addx/noop
instructions. Compute sum of signal strength (cycle * X) at cycles 20, 60,
100, 140, 180, and 220.
"""
from pathlib import Path

def ticks(s:str):
    """Yield X register value at each cycle as instructions execute."""
    x=1
    for ln in s.splitlines():
        if not ln: continue
        if ln=='noop':
            yield x
        else:
            _,v=ln.split(); v=int(v)
            yield x; yield x
            x+=v

def solve(s:str)->int:
    """Solve Part 1: sum signal strength at specified cycles."""
    vals=list(ticks(s))
    return sum(i*vals[i-1] for i in [20,60,100,140,180,220])

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d10_input.txt').read_text()))
