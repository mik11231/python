#!/usr/bin/env python3
"""Advent of Code 2022 Day 20 Part 1.

Grove Positioning System: mix numbers by moving each in order by its value.
Each number moves forward/backward by its value (mod n-1). Returns sum of
values at positions 1000, 2000, 3000 after the 0.
"""
from pathlib import Path

def mix(nums,rounds=1,key=1):
    """Mix the list by moving each element by its (scaled) value, return grove sum."""
    arr=[(i,n*key) for i,n in enumerate(nums)]
    order=arr.copy(); n=len(arr)
    for _ in range(rounds):
        for item in order:
            i=arr.index(item)
            arr.pop(i)
            j=(i+item[1])%(n-1)
            arr.insert(j,item)
    vals=[v for _,v in arr]
    z=vals.index(0)
    return vals[(z+1000)%n]+vals[(z+2000)%n]+vals[(z+3000)%n]

def solve(s):
    """Parse numbers and return grove coordinate sum after one mix round."""
    nums=[int(x) for x in s.splitlines() if x]
    return mix(nums,1,1)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d20_input.txt').read_text()))
