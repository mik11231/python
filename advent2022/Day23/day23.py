#!/usr/bin/env python3
"""Advent of Code 2022 Day 23 Part 1.

Unstable Diffusion: elves propose moves in rotating N/S/W/E order. Each round,
elves with neighbors propose moving in first valid direction; conflicts cancel.
After 10 rounds, return empty tiles in bounding rectangle.
"""
from pathlib import Path
from collections import Counter

DIRCHK=[
    ((0,-1), [(-1,-1),(0,-1),(1,-1)]),
    ((0,1),  [(-1,1),(0,1),(1,1)]),
    ((-1,0), [(-1,-1),(-1,0),(-1,1)]),
    ((1,0),  [(1,-1),(1,0),(1,1)]),
]


def parse(s):
    """Parse grid and return set of (x,y) elf positions."""
    e=set()
    for y,r in enumerate(s.splitlines()):
        for x,c in enumerate(r.strip()):
            if c=='#': e.add((x,y))
    return e

def round_(elves,off):
    """Run one round of elf movement; return (new positions, whether any moved)."""
    prop={}
    cnt=Counter()
    for x,y in elves:
        nbr=False
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if (dx,dy)!=(0,0) and (x+dx,y+dy) in elves: nbr=True
        if not nbr: continue
        for k in range(4):
            mv,chk=DIRCHK[(off+k)%4]
            if all((x+dx,y+dy) not in elves for dx,dy in chk):
                nx,ny=x+mv[0],y+mv[1]
                prop[(x,y)]=(nx,ny); cnt[(nx,ny)]+=1; break
    moved=False
    out=set(elves)
    for src,dst in prop.items():
        if cnt[dst]==1:
            out.remove(src); out.add(dst); moved=True
    return out,moved

def solve(s):
    """Parse elves, run 10 rounds, return empty tiles in bounding box."""
    e=parse(s)
    off=0
    for _ in range(10):
        e,_=round_(e,off); off=(off+1)%4
    xs=[x for x,y in e]; ys=[y for x,y in e]
    area=(max(xs)-min(xs)+1)*(max(ys)-min(ys)+1)
    return area-len(e)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d23_input.txt').read_text()))
