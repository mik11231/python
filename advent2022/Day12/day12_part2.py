#!/usr/bin/env python3
"""Advent of Code 2022 Day 12 Part 2.

Find shortest path from any 'a' to E. Reverse BFS from E: step down only when
target elevation is at most 1 lower. First 'a' reached gives the answer.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.grid import neighbors4
from aoclib.search import bfs_distances

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
    def _reverse_neighbors(cell):
        x, y = cell
        for ny, nx in neighbors4(y, x, h, w):
            if ht(g[ny][nx]) >= ht(g[y][x]) - 1:
                yield (nx, ny)

    dist = bfs_distances(en, _reverse_neighbors)
    return min(d for (x, y), d in dist.items() if ht(g[y][x]) == ord('a'))

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d12_input.txt').read_text()))
