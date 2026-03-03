#!/usr/bin/env python3
"""Advent of Code 2022 Day 1 Part 1.

Calorie counting: elves carry food items with calories. Find the elf carrying
the most total calories. Input is groups of numbers separated by blank lines.
Algorithm: split by double newlines, sum each group, return the maximum.
"""
from pathlib import Path

def solve(s:str)->int:
    """Return the maximum total calories carried by any single elf."""
    groups=s.strip().split('\n\n')
    return max(sum(map(int,g.splitlines())) for g in groups)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d1_input.txt').read_text()))
