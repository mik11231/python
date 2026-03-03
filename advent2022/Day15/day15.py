#!/usr/bin/env python3
"""Advent of Code 2022 Day 15 Part 1.

Beacon Exclusion Zone: sensors report Manhattan distance to nearest beacon.
For a given row, compute intervals where a beacon cannot exist, merge them,
and subtract positions already occupied by beacons in that row.
"""
from pathlib import Path
import re

def solve(s,row=2000000):
    """Solve Part 1: count positions in given row that cannot contain a beacon."""
    sens=[]; beacons=set()
    for ln in s.splitlines():
        if not ln: continue
        sx,sy,bx,by=map(int,re.findall(r'-?\d+',ln))
        d=abs(sx-bx)+abs(sy-by)
        sens.append((sx,sy,d))
        if by==row: beacons.add(bx)
    ints=[]
    for sx,sy,d in sens:
        rem=d-abs(sy-row)
        if rem>=0: ints.append((sx-rem,sx+rem))
    ints.sort()
    merged=[]
    for a,b in ints:
        if not merged or a>merged[-1][1]+1: merged.append([a,b])
        else: merged[-1][1]=max(merged[-1][1],b)
    total=sum(b-a+1 for a,b in merged)
    total-=sum(any(a<=x<=b for a,b in merged) for x in beacons)
    return total

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d15_input.txt').read_text(),2000000))
