#!/usr/bin/env python3
"""Advent of Code 2022 Day 8 Part 2.

Treetop Tree House: scenic score = product of viewing distances in four
directions (trees until blocked or edge). Find maximum scenic score.
Algorithm: for each tree, count visible trees in each direction, multiply.
"""
from pathlib import Path

def solve(s:str)->int:
    """Return the maximum scenic score of any tree in the grid."""
    g=[[int(c) for c in ln.strip()] for ln in s.splitlines() if ln.strip()]
    h,w=len(g),len(g[0])
    best=0
    for y in range(h):
        for x in range(w):
            v=g[y][x]
            a=b=c=d=0
            for i in range(x-1,-1,-1):
                a+=1
                if g[y][i]>=v: break
            for i in range(x+1,w):
                b+=1
                if g[y][i]>=v: break
            for j in range(y-1,-1,-1):
                c+=1
                if g[j][x]>=v: break
            for j in range(y+1,h):
                d+=1
                if g[j][x]>=v: break
            best=max(best,a*b*c*d)
    return best

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d8_input.txt').read_text()))
