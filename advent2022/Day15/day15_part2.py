#!/usr/bin/env python3
"""Advent of Code 2022 Day 15 Part 2.

Find the single empty position in [0,lim]x[0,lim] not covered by any sensor.
Scan rows and find the first gap in merged exclusion intervals; tuning
frequency is x*4000000+y.
"""
from pathlib import Path
import re

def solve(s,lim=4000000):
    """Solve Part 2: find hidden beacon and return tuning frequency."""
    sens=[]
    for ln in s.splitlines():
        if not ln: continue
        sx,sy,bx,by=map(int,re.findall(r'-?\d+',ln))
        d=abs(sx-bx)+abs(sy-by)
        sens.append((sx,sy,d))
    for y in range(lim+1):
        ints=[]
        for sx,sy,d in sens:
            rem=d-abs(sy-y)
            if rem>=0:
                a=max(0,sx-rem); b=min(lim,sx+rem)
                ints.append((a,b))
        ints.sort()
        x=0
        for a,b in ints:
            if a>x:
                return x*4000000+y
            x=max(x,b+1)
            if x>lim: break
        if x<=lim:
            return x*4000000+y
    raise RuntimeError

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d15_input.txt').read_text(),4000000))
