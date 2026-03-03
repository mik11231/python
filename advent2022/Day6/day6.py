#!/usr/bin/env python3
"""Advent of Code 2022 Day 6 Part 1.

Tuning trouble: find the first position where 4 consecutive characters are all
different (start-of-packet marker). Algorithm: sliding window of size k, return
index when window has k distinct chars.
"""
from pathlib import Path

def first_marker(s:str,k:int)->int:
    """Return the 1-based index of the first k-length substring with k distinct chars."""
    for i in range(k,len(s)+1):
        if len(set(s[i-k:i]))==k: return i
    raise RuntimeError

def solve(s:str)->int:
    """Return position of first start-of-packet marker (4 distinct chars)."""
    return first_marker(s.strip(),4)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d6_input.txt').read_text()))
