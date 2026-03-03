#!/usr/bin/env python3
"""Advent of Code 2022 Day 11 Part 1.

Monkey in the Middle: parse monkeys with items, operations, and test rules.
Simulate 20 rounds of item passing; worry is divided by 3 after inspection.
Return product of the two highest inspection counts.
"""
from pathlib import Path
import math


def parse(s):
    """Parse input into list of monkeys: [items, op, div, true_idx, false_idx, count]."""
    ms=[]
    for blk in s.strip().split('\n\n'):
        ls=blk.splitlines()
        items=list(map(int,ls[1].split(': ')[1].split(', ')))
        op=ls[2].split('= ')[1].split()
        div=int(ls[3].split()[-1])
        t=int(ls[4].split()[-1]); f=int(ls[5].split()[-1])
        ms.append([items,op,div,t,f,0])
    return ms

def apply(old,op):
    """Apply monkey operation (add or multiply) to old worry value."""
    a,b,c=op
    x=old if c=='old' else int(c)
    return old+x if b=='+' else old*x

def run(ms,rounds,relief=True):
    """Run simulation for given rounds; relief=True divides by 3, else uses modulo."""
    mod=math.prod(m[2] for m in ms)
    for _ in range(rounds):
        for m in ms:
            items,op,div,t,f,_=m
            while items:
                m[5]+=1
                v=apply(items.pop(0),op)
                if relief: v//=3
                else: v%=mod
                ms[t if v%div==0 else f][0].append(v)
    c=sorted((m[5] for m in ms), reverse=True)
    return c[0]*c[1]

def solve(s):
    """Solve Part 1: 20 rounds with worry relief, return monkey business."""
    return run(parse(s),20,True)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d11_input.txt').read_text()))
