#!/usr/bin/env python3
"""Advent of Code 2022 Day 22 Part 2.

Same map but the grid folds into a cube. Uses hardcoded face transitions for
the real input's 50x50 cube net layout (A,B,C,D,E,F faces).
"""
from pathlib import Path
import re

DIRS=[(1,0),(0,1),(-1,0),(0,-1)]  # R,D,L,U


def parse(s):
    """Parse grid and movement tokens from input."""
    a,b=s.rstrip().split('\n\n')
    rows=a.splitlines()
    w=max(len(r) for r in rows)
    g=[r.ljust(w) for r in rows]
    toks=re.findall(r'\d+|[LR]', b.strip())
    return g,toks


def wrap(x,y,d):
    """Return (nx, ny, nd) when stepping off edge onto adjacent cube face."""
    #   A B
    #   C
    # D E
    # F
    # A: x 50..99 y 0..49
    # B: x100..149 y 0..49
    # C: x 50..99 y50..99
    # D: x  0..49 y100..149
    # E: x 50..99 y100..149
    # F: x  0..49 y150..199

    if d==3:  # moving up
        if 50<=x<=99 and y==0:      # A -> F (left edge)
            return 0, x+100, 0
        if 100<=x<=149 and y==0:    # B -> F (bottom edge)
            return x-100, 199, 3
        if 0<=x<=49 and y==100:     # D -> C (left edge)
            return 50, x+50, 0
    elif d==1:  # moving down
        if 100<=x<=149 and y==49:   # B -> C (right edge)
            return 99, x-50, 2
        if 50<=x<=99 and y==149:    # E -> F (right edge)
            return 49, x+100, 2
        if 0<=x<=49 and y==199:     # F -> B (top edge)
            return x+100, 0, 1
    elif d==2:  # moving left
        if 50<=y<=99 and x==50:     # C -> D (top edge)
            return y-50, 100, 1
        if 0<=y<=49 and x==50:      # A -> D (left edge mirrored)
            return 0, 149-y, 0
        if 150<=y<=199 and x==0:    # F -> A (top edge)
            return y-100, 0, 1
        if 100<=y<=149 and x==0:    # D -> A (left edge mirrored)
            return 50, 149-y, 0
    else:  # d==0 moving right
        if 0<=y<=49 and x==149:     # B -> E (right edge mirrored)
            return 99, 149-y, 2
        if 50<=y<=99 and x==99:     # C -> B (bottom edge)
            return y+50, 49, 3
        if 100<=y<=149 and x==99:   # E -> B (right edge mirrored)
            return 149, 149-y, 2
        if 150<=y<=199 and x==49:   # F -> E (bottom edge)
            return y-100, 149, 3

    raise RuntimeError(f'unhandled wrap {x,y,d}')


def solve(s):
    """Parse input, follow path with cube wrapping, return password."""
    g,toks=parse(s)
    y=0; x=g[0].index('.')
    d=0

    for t in toks:
        if t=='L': d=(d-1)%4; continue
        if t=='R': d=(d+1)%4; continue
        n=int(t)
        for _ in range(n):
            dx,dy=DIRS[d]
            nx,ny,nd=x+dx,y+dy,d
            if not (0<=ny<len(g) and 0<=nx<len(g[0])) or g[ny][nx]==' ':
                nx,ny,nd=wrap(x,y,d)
            if g[ny][nx]=='#':
                break
            x,y,d=nx,ny,nd

    return 1000*(y+1)+4*(x+1)+d


if __name__=='__main__':
    print(solve(Path(__file__).with_name('d22_input.txt').read_text()))
