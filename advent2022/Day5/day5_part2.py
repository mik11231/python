#!/usr/bin/env python3
"""Advent of Code 2022 Day 5 Part 2.

Supply stacks: CrateMover 9001 moves multiple crates at once, preserving order.
Algorithm: same parsing as part 1; apply moves by slicing blocks and extending
the destination stack.
"""
from pathlib import Path
import re

def parse(s:str):
    """Parse input into stacks (list of lists) and moves (count, from, to)."""
    a,b=s.split('\n\n')
    rows=a.splitlines()
    n=int(rows[-1].split()[-1])
    stacks=[[] for _ in range(n)]
    for r in rows[-2::-1]:
        for i in range(n):
            j=1+4*i
            if j<len(r) and r[j]!=' ': stacks[i].append(r[j])
    moves=[tuple(map(int,re.findall(r'\d+',ln))) for ln in b.splitlines() if ln]
    return stacks,moves

def solve(s:str)->str:
    """Return the top crate of each stack after moving blocks as a unit."""
    stacks,moves=parse(s)
    for c,a,b in moves:
        block=stacks[a-1][-c:]
        stacks[a-1]=stacks[a-1][:-c]
        stacks[b-1].extend(block)
    return ''.join(st[-1] for st in stacks)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d5_input.txt').read_text()))
