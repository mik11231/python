#!/usr/bin/env python3
"""Advent of Code 2022 Day 13 Part 1.

Distress Signal: compare packet pairs (lists/ints) using recursive ordering
rules. Sum the 1-based indices of pairs that are in the correct order.
"""
from pathlib import Path
import ast

def cmp(a,b):
    """Compare two packets; returns negative if a<b, 0 if equal, positive if a>b."""
    if isinstance(a,int) and isinstance(b,int): return (a>b)-(a<b)
    if isinstance(a,int): a=[a]
    if isinstance(b,int): b=[b]
    for x,y in zip(a,b):
        c=cmp(x,y)
        if c: return c
    return (len(a)>len(b))-(len(a)<len(b))

def solve(s):
    """Solve Part 1: sum indices of correctly ordered pairs."""
    ans=0
    for i,blk in enumerate(s.strip().split('\n\n'),1):
        a,b=map(ast.literal_eval,blk.splitlines())
        if cmp(a,b)<0: ans+=i
    return ans

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d13_input.txt').read_text()))
