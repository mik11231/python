#!/usr/bin/env python3
"""Advent of Code 2022 Day 2 Part 2.

Rock Paper Scissors: X/Y/Z mean lose/draw/win. Choose our move accordingly.
Algorithm: map opponent choice to 0/1/2, derive our move from desired outcome
using modular arithmetic, accumulate score.
"""
from pathlib import Path

def solve(s:str)->int:
    """Return total score when X/Y/Z mean lose/draw/win."""
    them_map={'A':0,'B':1,'C':2}
    # X lose, Y draw, Z win
    score=0
    for ln in s.splitlines():
        if not ln.strip(): continue
        a,b=ln.split()
        t=them_map[a]
        if b=='X':
            m=(t-1)%3; score+=0
        elif b=='Y':
            m=t; score+=3
        else:
            m=(t+1)%3; score+=6
        score+=m+1
    return score

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d2_input.txt').read_text()))
