#!/usr/bin/env python3
"""Advent of Code 2022 Day 15 Part 1.

Beacon Exclusion Zone: sensors report Manhattan distance to nearest beacon.
For a given row, compute intervals where a beacon cannot exist, merge them,
and subtract positions already occupied by beacons in that row.
"""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.geometry import manhattan2
from aoclib.intervals import covered_length, merge_intervals

def solve(s,row=2000000):
    """Solve Part 1: count positions in given row that cannot contain a beacon."""
    sens=[]; beacons=set()
    for ln in s.splitlines():
        if not ln: continue
        sx,sy,bx,by=map(int,re.findall(r'-?\d+',ln))
        d = manhattan2((sx, sy), (bx, by))
        sens.append((sx,sy,d))
        if by==row: beacons.add(bx)
    ints=[]
    for sx,sy,d in sens:
        rem=d-abs(sy-row)
        if rem>=0: ints.append((sx-rem,sx+rem))
    merged = merge_intervals(ints, touch=True)
    total = covered_length(ints, touch=True)
    total-=sum(any(a<=x<=b for a,b in merged) for x in beacons)
    return total

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d15_input.txt').read_text(),2000000))
