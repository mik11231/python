#!/usr/bin/env python3
"""Advent of Code 2022 Day 18 Part 1.

Boiling Boulders: count surface area of lava droplet formed by 1x1 cubes.
Each cube face not touching another cube counts toward the total surface area.
"""
from pathlib import Path

def solve(s):
    """Parse cube coordinates and return total exposed surface area."""
    cubes={tuple(map(int,ln.split(','))) for ln in s.splitlines() if ln}
    ans=0
    for x,y,z in cubes:
        for dx,dy,dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            if (x+dx,y+dy,z+dz) not in cubes: ans+=1
    return ans

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d18_input.txt').read_text()))
