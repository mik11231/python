#!/usr/bin/env python3
"""Advent of Code 2022 Day 22 Part 1.

Monkey Map: walk a 2D grid following move/rotate instructions. Wrapping is
flat (wrap to opposite edge on same row/column). Returns password from
final position and facing.
"""
from pathlib import Path
import re

DIRS=[(1,0),(0,1),(-1,0),(0,-1)]

def parse(s):
    """Parse grid and movement tokens from input."""
    a,b=s.rstrip().split('\n\n')
    rows=a.splitlines()
    w=max(len(r) for r in rows)
    g=[r.ljust(w) for r in rows]
    toks=re.findall(r'\d+|[LR]', b.strip())
    return g,toks

def solve(s):
    """Parse input, follow path with flat wrapping, return password."""
    g,toks=parse(s)
    h,w=len(g),len(g[0])
    y=0; x=g[0].index('.')
    d=0
    for t in toks:
        if t=='L': d=(d-1)%4; continue
        if t=='R': d=(d+1)%4; continue
        n=int(t)
        dx,dy=DIRS[d]
        for _ in range(n):
            nx,ny=x+dx,y+dy
            if not (0<=nx<w and 0<=ny<h) or g[ny][nx]==' ':
                # wrap
                if d==0:
                    nx=next(i for i,c in enumerate(g[y]) if c!=' '); ny=y
                elif d==2:
                    nx=max(i for i,c in enumerate(g[y]) if c!=' '); ny=y
                elif d==1:
                    ny=next(i for i in range(h) if g[i][x]!=' '); nx=x
                else:
                    ny=max(i for i in range(h) if g[i][x]!=' '); nx=x
            if g[ny][nx]=='#':
                break
            x,y=nx,ny
    return 1000*(y+1)+4*(x+1)+d

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d22_input.txt').read_text()))
