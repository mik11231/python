#!/usr/bin/env python3
"""Advent of Code 2022 Day 12 Part 2.

Find shortest path from any 'a' to E. Reverse BFS from E: step down only when
target elevation is at most 1 lower. First 'a' reached gives the answer.
"""
from collections import deque
from pathlib import Path

def solve(s):
    """Solve Part 2: reverse BFS from E to nearest 'a', return fewest steps."""
    g=[list(r.strip()) for r in s.splitlines() if r.strip()]
    h,w=len(g),len(g[0])
    for y in range(h):
        for x in range(w):
            if g[y][x]=='E': en=(x,y)
    def ht(c):
        """Map cell character to elevation (a=0, z=25)."""
        if c=='S': return ord('a')
        if c=='E': return ord('z')
        return ord(c)
    # reverse BFS from end
    q=deque([(en,0)]); seen={en}
    while q:
        (x,y),d=q.popleft()
        if ht(g[y][x])==ord('a'): return d
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if 0<=nx<w and 0<=ny<h and (nx,ny) not in seen:
                if ht(g[ny][nx])>=ht(g[y][x])-1:
                    seen.add((nx,ny)); q.append(((nx,ny),d+1))

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d12_input.txt').read_text()))
