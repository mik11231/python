#!/usr/bin/env python3
"""Advent of Code 2022 Day 25 Part 2.

Day 25 has no separate computational Part 2; reuses Part 1 solution.
"""
from pathlib import Path
from day25 import solve

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d25_input.txt').read_text()))
