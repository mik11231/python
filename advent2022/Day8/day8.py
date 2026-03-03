#!/usr/bin/env python3
"""Advent of Code 2022 Day 8 Part 1.

Treetop Tree House: grid of tree heights. Count trees visible from outside
(visible if shorter than it in at least one of the four cardinal directions).
Algorithm: for each tree, check if it's the max in any direction.
"""
from pathlib import Path

def solve(s:str)->int:
    """Return count of trees visible from outside the grid."""
    g=[[int(c) for c in ln.strip()] for ln in s.splitlines() if ln.strip()]
    h,w=len(g),len(g[0])
    ans=0
    for y in range(h):
        for x in range(w):
            v=g[y][x]
            if all(g[y][i]<v for i in range(x)) or all(g[y][i]<v for i in range(x+1,w)) or all(g[j][x]<v for j in range(y)) or all(g[j][x]<v for j in range(y+1,h)):
                ans+=1
    return ans

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d8_input.txt').read_text()))
