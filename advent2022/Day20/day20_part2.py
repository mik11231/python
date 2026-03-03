#!/usr/bin/env python3
"""Advent of Code 2022 Day 20 Part 2.

Same mixing but with decryption key 811589153 and 10 rounds of mixing.
"""
from pathlib import Path
from day20 import mix

def solve(s):
    """Parse numbers, mix 10 rounds with key 811589153, return grove sum."""
    nums=[int(x) for x in s.splitlines() if x]
    return mix(nums,10,811589153)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d20_input.txt').read_text()))
