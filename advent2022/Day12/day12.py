#!/usr/bin/env python3
"""Advent of Code 2022 Day 12 Part 1.

Hill Climbing: find shortest path from S to E on an elevation grid. Can only
step to adjacent cells if target elevation is at most 1 higher. Uses BFS.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.grid import neighbors4
from aoclib.search import bfs_distances

def solve(s):
    """Solve Part 1: BFS from S to E, return fewest steps."""
    g=[list(r.strip()) for r in s.splitlines() if r.strip()]
    h,w=len(g),len(g[0])
    for y in range(h):
        for x in range(w):
            if g[y][x]=='S': st=(x,y)
            if g[y][x]=='E': en=(x,y)
    def ht(c):
        """Map cell character to elevation (a=0, z=25)."""
        if c=='S': return ord('a')
        if c=='E': return ord('z')
        return ord(c)
    def _neighbors(cell):
        """
        Run `_neighbors` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: cell.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        x, y = cell
        for ny, nx in neighbors4(y, x, h, w):
            if ht(g[ny][nx]) <= ht(g[y][x]) + 1:
                yield (nx, ny)

    dist = bfs_distances(st, _neighbors)
    return dist[en]

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d12_input.txt').read_text()))
