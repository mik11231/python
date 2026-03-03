#!/usr/bin/env python3
"""Advent of Code 2022 Day 9 Part 1.

Rope Bridge: simulate a rope with n knots where the head follows motion
commands and each knot follows the previous. Count distinct positions visited
by the tail using Manhattan-distance following rules.
"""
from pathlib import Path

def sim(s:str,n=2):
    """Simulate rope motion and return count of distinct tail positions."""
    rope=[[0,0] for _ in range(n)]
    seen={(0,0)}
    step={'U':(0,1),'D':(0,-1),'L':(-1,0),'R':(1,0)}
    for ln in s.splitlines():
        if not ln: continue
        d,k=ln.split(); k=int(k)
        dx,dy=step[d]
        for _ in range(k):
            rope[0][0]+=dx; rope[0][1]+=dy
            for i in range(1,n):
                hx,hy=rope[i-1]; tx,ty=rope[i]
                ddx,ddy=hx-tx,hy-ty
                if abs(ddx)>1 or abs(ddy)>1:
                    rope[i][0]+=0 if ddx==0 else (1 if ddx>0 else -1)
                    rope[i][1]+=0 if ddy==0 else (1 if ddy>0 else -1)
            seen.add(tuple(rope[-1]))
    return len(seen)

def solve(s:str)->int:
    """Solve Part 1: count tail positions for a 2-knot rope."""
    return sim(s,2)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d9_input.txt').read_text()))
