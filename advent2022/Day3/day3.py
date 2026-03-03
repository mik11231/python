#!/usr/bin/env python3
"""Advent of Code 2022 Day 3 Part 1.

Rucksack reorganization: each line has two compartments; find the item type
appearing in both halves. Priority: a-z=1-26, A-Z=27-52. Algorithm: split each
line in half, intersect sets, sum priorities.
"""
from pathlib import Path

def pri(c):
    """Return priority 1-52 for a-z or A-Z."""
    return ord(c)-96 if 'a'<=c<='z' else ord(c)-38

def solve(s:str)->int:
    """Return sum of priorities of items in both compartments of each rucksack."""
    ans=0
    for ln in s.splitlines():
        if not ln: continue
        n=len(ln)//2
        c=(set(ln[:n]) & set(ln[n:])).pop()
        ans+=pri(c)
    return ans

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d3_input.txt').read_text()))
