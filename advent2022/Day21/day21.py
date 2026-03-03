#!/usr/bin/env python3
"""Advent of Code 2022 Day 21 Part 1.

Monkey Math: monkeys yell numbers or binary expressions (+, -, *, /).
Parse the tree and evaluate root's value recursively with caching.
"""
from pathlib import Path

def parse(s):
    """Parse input into a dict of monkey name -> value or expression."""
    m={}
    for ln in s.splitlines():
        if not ln: continue
        k,v=ln.split(': ')
        m[k]=v
    return m

def evaln(name,m,cache):
    """Recursively evaluate a monkey's value, using cache for memoization."""
    if name in cache: return cache[name]
    v=m[name]
    if v.lstrip('-').isdigit():
        cache[name]=int(v); return cache[name]
    a,op,b=v.split()
    x,y=evaln(a,m,cache),evaln(b,m,cache)
    cache[name]= {'+':x+y,'-':x-y,'*':x*y,'/':x//y}[op]
    return cache[name]

def solve(s):
    """Parse and return root monkey's evaluated value."""
    m=parse(s)
    return evaln('root',m,{})

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d21_input.txt').read_text()))
