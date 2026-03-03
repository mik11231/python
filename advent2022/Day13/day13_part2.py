#!/usr/bin/env python3
"""Advent of Code 2022 Day 13 Part 2.

Sort all packets plus divider packets [[2]] and [[6]]; return product of
their 1-based indices in the sorted list.
"""
from pathlib import Path
import ast
from functools import cmp_to_key
from day13 import cmp

def solve(s):
    """Solve Part 2: sort packets with dividers, return decoder key."""
    ps=[ast.literal_eval(ln) for ln in s.splitlines() if ln.strip()]
    a=[[2]]; b=[[6]]
    ps.extend([a,b])
    ps.sort(key=cmp_to_key(cmp))
    return (ps.index(a)+1)*(ps.index(b)+1)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d13_input.txt').read_text()))
