#!/usr/bin/env python3
"""Advent of Code 2022 Day 2 Part 1.

Rock Paper Scissors: A/B/C = opponent's rock/paper/scissors, X/Y/Z = our choice.
Score = shape (1/2/3) + outcome (0/3/6). Algorithm: map choices to 0/1/2, compute
outcome via modular arithmetic, accumulate score.
"""
from pathlib import Path

def solve(s:str)->int:
    """Return total score when X/Y/Z mean our rock/paper/scissors choice."""
    # A/B/C = rock/paper/scissors, X/Y/Z = rock/paper/scissors
    them_map={'A':0,'B':1,'C':2}
    me_map={'X':0,'Y':1,'Z':2}
    score=0
    for ln in s.splitlines():
        if not ln.strip(): continue
        a,b=ln.split()
        t,m=them_map[a],me_map[b]
        score+=m+1
        if m==t: score+=3
        elif (m-t)%3==1: score+=6
    return score

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d2_input.txt').read_text()))
