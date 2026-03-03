#!/usr/bin/env python3
"""Advent of Code 2022 Day 25 Part 1.

Full of Hot Air: SNAFU is base-5 with digits 2,1,0,-,=. Convert each line
from SNAFU to decimal, sum, and convert the sum back to SNAFU.
"""
from pathlib import Path

MAP={'2':2,'1':1,'0':0,'-':-1,'=':-2}
RMAP={0:'0',1:'1',2:'2',3:'=',4:'-'}

def from_snafu(s):
    """Convert SNAFU string to decimal integer."""
    v=0
    for c in s:
        v=v*5+MAP[c]
    return v

def to_snafu(n):
    """Convert decimal integer to SNAFU string."""
    if n==0: return '0'
    out=[]
    while n:
        n,r=divmod(n,5)
        out.append(RMAP[r])
        if r>=3: n+=1
    return ''.join(reversed(out))

def solve(s):
    """Parse SNAFU numbers, sum them, return sum in SNAFU."""
    return to_snafu(sum(from_snafu(ln.strip()) for ln in s.splitlines() if ln.strip()))

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d25_input.txt').read_text()))
