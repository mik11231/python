#!/usr/bin/env python3
"""Advent of Code 2022 Day 24 Part 1.

Blizzard Basin: navigate from start to end avoiding moving blizzards. Blizzards
repeat on a cycle (LCM of width and height). BFS with precomputed occupancy
per time mod cycle to find shortest path.
"""
from collections import deque
from pathlib import Path
import math


def parse(s):
    """Parse grid, start/end, and blizzard positions and directions."""
    g=[list(r) for r in s.splitlines() if r]
    h,w=len(g),len(g[0])
    start=(g[0].index('.'),0)
    end=(g[-1].index('.'),h-1)
    bl=[]
    for y in range(h):
        for x in range(w):
            c=g[y][x]
            if c in '<>^v': bl.append((x,y,c))
    return w,h,start,end,bl


def precompute(w,h,bl):
    """Precompute occupied cells for each time t mod cycle length."""
    W,H=w-2,h-2
    mod=math.lcm(W,H)
    occ=[set() for _ in range(mod)]
    for t in range(mod):
        s=occ[t]
        for x,y,c in bl:
            if c=='>': nx=1+((x-1+t)%W); ny=y
            elif c=='<': nx=1+((x-1-t)%W); ny=y
            elif c=='v': nx=x; ny=1+((y-1+t)%H)
            else: nx=x; ny=1+((y-1-t)%H)
            s.add((nx,ny))
    return occ,mod


def trip(st,en,t0,w,h,occ,mod):
    """BFS from st to en starting at time t0; return arrival time."""
    q=deque([(st[0],st[1],t0)])
    seen={(st[0],st[1],t0%mod)}
    while q:
        x,y,t=q.popleft()
        nt=t+1
        blk=occ[nt%mod]
        for nx,ny in [(x,y),(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if (nx,ny)==en and (nx,ny) not in blk:
                return nt
            if (nx,ny)==st and (nx,ny) not in blk:
                key=(nx,ny,nt%mod)
                if key not in seen:
                    seen.add(key); q.append((nx,ny,nt))
                continue
            if not (1<=nx<=w-2 and 1<=ny<=h-2):
                continue
            if (nx,ny) in blk:
                continue
            key=(nx,ny,nt%mod)
            if key not in seen:
                seen.add(key); q.append((nx,ny,nt))
    raise RuntimeError


def solve(s):
    """Parse input, precompute blizzard positions, return time to reach end."""
    w,h,st,en,bl=parse(s)
    occ,mod=precompute(w,h,bl)
    return trip(st,en,0,w,h,occ,mod)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d24_input.txt').read_text()))
