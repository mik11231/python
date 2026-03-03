#!/usr/bin/env python3
"""Advent of Code 2022 Day 14 Part 1.

Regolith Reservoir: parse rock paths and simulate sand falling from (500,0).
Sand falls down/diagonally until it rests or falls into the abyss. Count
grains that come to rest before any falls past the lowest rock.
"""
from pathlib import Path

def parse(s):
    """Parse rock paths into a set of coordinates and max y; return (rock, maxy)."""
    rock=set(); maxy=0
    for ln in s.splitlines():
        if not ln: continue
        pts=[tuple(map(int,p.split(','))) for p in ln.split(' -> ')]
        for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
            if x1==x2:
                for y in range(min(y1,y2),max(y1,y2)+1): rock.add((x1,y)); maxy=max(maxy,y)
            else:
                for x in range(min(x1,x2),max(x1,x2)+1): rock.add((x,y1)); maxy=max(maxy,y1)
    return rock,maxy

def solve(s):
    """Solve Part 1: count sand grains before any falls into abyss."""
    rock,maxy=parse(s)
    sand=set(); src=(500,0)
    while True:
        x,y=src
        while True:
            if y>maxy: return len(sand)
            if (x,y+1) not in rock and (x,y+1) not in sand: y+=1; continue
            if (x-1,y+1) not in rock and (x-1,y+1) not in sand: x-=1; y+=1; continue
            if (x+1,y+1) not in rock and (x+1,y+1) not in sand: x+=1; y+=1; continue
            sand.add((x,y)); break

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d14_input.txt').read_text()))
