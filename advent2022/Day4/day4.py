#!/usr/bin/env python3
"""Advent of Code 2022 Day 4 Part 1.

Camp cleanup: pairs of assignment ranges (a-b,c-d). Count pairs where one range
fully contains the other. Algorithm: parse ranges, check if one contains the
other (a1<=b1 and a2>=b2, or vice versa).
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.intervals import contains_interval, parse_int_range

def solve(s:str)->int:
    """Return count of pairs where one range fully contains the other."""
    ans=0
    for ln in s.splitlines():
        if not ln: continue
        a,b=ln.split(',')
        ra = parse_int_range(a)
        rb = parse_int_range(b)
        if contains_interval(ra, rb) or contains_interval(rb, ra): ans+=1
    return ans

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d4_input.txt').read_text()))
