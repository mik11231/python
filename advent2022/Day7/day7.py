#!/usr/bin/env python3
"""Advent of Code 2022 Day 7 Part 1.

No Space Left On Device: parse shell output (cd, ls) to build directory tree.
Sum sizes of directories with total size at most 100000. Algorithm: track cwd,
accumulate file sizes into all ancestor directories, sum those <= 100000.
"""
from pathlib import Path
from collections import defaultdict

def sizes(s:str):
    """Parse shell output and return dict mapping directory path tuple to total size."""
    cwd=[]
    sz=defaultdict(int)
    for ln in s.splitlines():
        if ln.startswith('$ cd '):
            d=ln[5:]
            if d=='/': cwd=['/']
            elif d=='..': cwd.pop()
            else: cwd.append(d)
        elif ln and ln[0].isdigit():
            n=int(ln.split()[0])
            for i in range(1,len(cwd)+1):
                sz[tuple(cwd[:i])] += n
    return sz

def solve(s:str)->int:
    """Return sum of directory sizes that are at most 100000."""
    return sum(v for v in sizes(s).values() if v<=100000)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d7_input.txt').read_text()))
