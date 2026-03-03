#!/usr/bin/env python3
"""Advent of Code 2022 Day 17 Part 1.

Pyroclastic Flow: rocks fall in a 7-wide chamber, pushed by jet gusts.
Simulates 2022 rocks falling and stacking; each rock is pushed then falls until
it rests. Returns the height of the tower after all rocks settle.
"""
from pathlib import Path

SHAPES=[
    [(0,0),(1,0),(2,0),(3,0)],
    [(1,0),(0,1),(1,1),(2,1),(1,2)],
    [(0,0),(1,0),(2,0),(2,1),(2,2)],
    [(0,0),(0,1),(0,2),(0,3)],
    [(0,0),(1,0),(0,1),(1,1)],
]

def sim(jets,rocks):
    """Simulate falling rocks and return the final tower height."""
    occ={(x,0) for x in range(7)}
    top=0; ji=0
    for i in range(rocks):
        sh=SHAPES[i%5]
        x,y=2,top+4
        while True:
            d=jets[ji%len(jets)]; ji+=1
            nx=x+(-1 if d=='<' else 1)
            if all(0<=nx+sx<7 and (nx+sx,y+sy) not in occ for sx,sy in sh): x=nx
            if all((x+sx,y+sy-1) not in occ for sx,sy in sh): y-=1
            else:
                for sx,sy in sh: occ.add((x+sx,y+sy)); top=max(top,y+sy)
                break
    return top

def solve(s):
    """Parse jet pattern and return height after 2022 rocks."""
    return sim(s.strip(),2022)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d17_input.txt').read_text()))
