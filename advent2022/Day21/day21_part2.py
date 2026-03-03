#!/usr/bin/env python3
"""Advent of Code 2022 Day 21 Part 2.

Find the number 'humn' must yell so root's two operands are equal.
Backpropagate the target value from root through the expression tree to humn.
"""
from functools import lru_cache
from pathlib import Path


def parse(s):
    """Parse input into a dict of monkey name -> value or expression."""
    m={}
    for ln in s.splitlines():
        if not ln: continue
        k,v=ln.split(': ')
        m[k]=v
    return m


def solve(s):
    """Parse, find which side of root has humn, backpropagate to get humn value."""
    m=parse(s)

    @lru_cache(None)
    def has_x(name):
        """Return True if this monkey's value depends on humn."""
        if name=='humn': return True
        v=m[name]
        if v.lstrip('-').isdigit(): return False
        a,_,b=v.split()
        return has_x(a) or has_x(b)

    @lru_cache(None)
    def val(name):
        """Evaluate monkey's value (assumes it does not depend on humn)."""
        v=m[name]
        if v.lstrip('-').isdigit(): return int(v)
        a,op,b=v.split()
        x,y=val(a),val(b)
        return {'+':x+y,'-':x-y,'*':x*y,'/':x//y}[op]

    def back(name,target):
        """Backpropagate target through expression tree to find humn."""
        if name=='humn': return target
        a,op,b=m[name].split()
        if has_x(a):
            k=val(b)
            if op=='+': return back(a,target-k)
            if op=='-': return back(a,target+k)
            if op=='*': return back(a,target//k)
            if op=='/': return back(a,target*k)
        else:
            k=val(a)
            if op=='+': return back(b,target-k)
            if op=='-': return back(b,k-target)
            if op=='*': return back(b,target//k)
            if op=='/': return back(b,k//target)
        raise RuntimeError

    l,_,r=m['root'].split()
    if has_x(l):
        return back(l,val(r))
    return back(r,val(l))


if __name__=='__main__':
    print(solve(Path(__file__).with_name('d21_input.txt').read_text()))
