#!/usr/bin/env python3
"""Advent of Code 2022 Day 14 Part 2.

Add an infinite floor at maxy+2; sand accumulates until it blocks the source
at (500,0). Count total grains of sand that come to rest.
"""
from pathlib import Path
from day14 import parse

def solve(s):
    """Solve Part 2: count sand until source is blocked by floor."""
    rock,maxy=parse(s)
    floor=maxy+2
    sand=set(); src=(500,0)
    while src not in sand:
        x,y=src
        while True:
            if y+1==floor: sand.add((x,y)); break
            if (x,y+1) not in rock and (x,y+1) not in sand: y+=1; continue
            if (x-1,y+1) not in rock and (x-1,y+1) not in sand: x-=1; y+=1; continue
            if (x+1,y+1) not in rock and (x+1,y+1) not in sand: x+=1; y+=1; continue
            sand.add((x,y)); break
    return len(sand)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d14_input.txt').read_text()))
