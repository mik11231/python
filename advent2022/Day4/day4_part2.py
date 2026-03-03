#!/usr/bin/env python3
"""Advent of Code 2022 Day 4 Part 2.

Camp cleanup: count pairs of ranges that overlap at all. Algorithm: parse
ranges, check overlap: ranges overlap iff not (a2<b1 or b2<a1).
"""
from pathlib import Path

def solve(s:str)->int:
    """Return count of pairs with any overlap."""
    ans=0
    for ln in s.splitlines():
        if not ln: continue
        a,b=ln.split(',')
        a1,a2=map(int,a.split('-')); b1,b2=map(int,b.split('-'))
        if not (a2<b1 or b2<a1): ans+=1
    return ans

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d4_input.txt').read_text()))
