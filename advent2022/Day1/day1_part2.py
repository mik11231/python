#!/usr/bin/env python3
"""Advent of Code 2022 Day 1 Part 2.

Calorie counting: find the sum of calories carried by the top 3 elves.
Algorithm: split by double newlines, sum each group, sort descending, sum top 3.
"""
from pathlib import Path

def solve(s:str)->int:
    """Return the sum of calories carried by the top 3 elves."""
    groups=s.strip().split('\n\n')
    vals=sorted((sum(map(int,g.splitlines())) for g in groups), reverse=True)
    return sum(vals[:3])

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d1_input.txt').read_text()))
