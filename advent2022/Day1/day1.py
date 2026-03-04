#!/usr/bin/env python3
"""Advent of Code 2022 Day 1 Part 1.

Calorie counting: elves carry food items with calories. Find the elf carrying
the most total calories. Input is groups of numbers separated by blank lines.
Algorithm: split by double newlines, sum each group, return the maximum.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.runner import print_answer, read_input_for

def solve(s:str)->int:
    """Return the maximum total calories carried by any single elf."""
    groups=s.strip().split('\n\n')
    return max(sum(map(int,g.splitlines())) for g in groups)

if __name__=='__main__':
    print_answer(solve(read_input_for(__file__, "d1_input.txt")))
