#!/usr/bin/env python3
"""Advent of Code 2022 Day 3 Part 2.

Rucksack reorganization: elves are in groups of 3; find the badge (common item)
in each group. Algorithm: process lines in triples, intersect the three sets,
sum priorities of the common item.
"""
from pathlib import Path

def pri(c):
    """Return priority 1-52 for a-z or A-Z."""
    return ord(c)-96 if 'a'<=c<='z' else ord(c)-38

def solve(s:str)->int:
    """Return sum of badge priorities for each group of 3 elves."""
    lines=[x for x in s.splitlines() if x]
    ans=0
    for i in range(0,len(lines),3):
        c=(set(lines[i])&set(lines[i+1])&set(lines[i+2])).pop()
        ans+=pri(c)
    return ans

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d3_input.txt').read_text()))
