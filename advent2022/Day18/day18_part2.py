#!/usr/bin/env python3
"""Advent of Code 2022 Day 18 Part 2.

Exterior surface only: air pockets inside the droplet don't count. BFS from a
point outside the bounding box to reach all exterior air; count faces where
exterior air touches a cube.
"""
from collections import deque
from pathlib import Path

def solve(s):
    """Parse cubes and return exterior surface area via BFS from outside."""
    cubes={tuple(map(int,ln.split(','))) for ln in s.splitlines() if ln}
    xs=[c[0] for c in cubes]; ys=[c[1] for c in cubes]; zs=[c[2] for c in cubes]
    minx,maxx=min(xs)-1,max(xs)+1
    miny,maxy=min(ys)-1,max(ys)+1
    minz,maxz=min(zs)-1,max(zs)+1

    q=deque([(minx,miny,minz)]); seen={(minx,miny,minz)}
    ans=0
    while q:
        x,y,z=q.popleft()
        for dx,dy,dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            nx,ny,nz=x+dx,y+dy,z+dz
            if not (minx<=nx<=maxx and miny<=ny<=maxy and minz<=nz<=maxz):
                continue
            p=(nx,ny,nz)
            if p in cubes: ans+=1
            elif p not in seen:
                seen.add(p); q.append(p)
    return ans

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d18_input.txt').read_text()))
