#!/usr/bin/env python3
"""Advent of Code 2022 Day 24 Part 2.

Three trips: start->end, end->start, start->end. Return total time for all three.
"""
from pathlib import Path
from day24 import parse, precompute, trip


def solve(s):
    """Parse input and return total time for start-end-start-end-start-end."""
    w,h,st,en,bl=parse(s)
    occ,mod=precompute(w,h,bl)
    t1=trip(st,en,0,w,h,occ,mod)
    t2=trip(en,st,t1,w,h,occ,mod)
    t3=trip(st,en,t2,w,h,occ,mod)
    return t3

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d24_input.txt').read_text()))
