#!/usr/bin/env python3
"""Advent of Code 2022 Day 15 Part 2.

Find the single empty position in [0,lim]x[0,lim] not covered by any sensor.
Scan rows and find the first gap in merged exclusion intervals; tuning
frequency is x*4000000+y.
"""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.geometry import manhattan2
from aoclib.intervals import clamp_interval, first_gap

def solve(s,lim=4000000):
    """Solve Part 2: find hidden beacon and return tuning frequency."""
    sens=[]
    for ln in s.splitlines():
        if not ln: continue
        sx,sy,bx,by=map(int,re.findall(r'-?\d+',ln))
        d = manhattan2((sx, sy), (bx, by))
        sens.append((sx,sy,d))
    for y in range(lim+1):
        ints=[]
        for sx,sy,d in sens:
            rem=d-abs(sy-y)
            if rem>=0:
                clipped = clamp_interval((sx-rem, sx+rem), 0, lim)
                if clipped is not None:
                    ints.append(clipped)
        x = first_gap(ints, 0, lim)
        if x is not None:
            return x*4000000+y
    raise RuntimeError

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d15_input.txt').read_text(),4000000))
