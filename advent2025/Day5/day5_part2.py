#!/usr/bin/env python3
"""Advent of Code 2025 - Day 5 Part 2: Cafeteria"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.intervals import covered_length

def solve():
    """Solve Day 5 Part 2: Count all unique fresh ingredient IDs."""
    # Read input
    with open(Path(__file__).with_name('d5_input.txt'), 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    # Parse ranges (only lines with '-')
    ranges = []
    for line in lines:
        if '-' in line:
            start, end = map(int, line.split('-'))
            ranges.append((start, end))
    
    return covered_length(ranges, touch=True)

if __name__ == "__main__":
    result = solve()
    print(f"The total number of fresh ingredient IDs is: {result}")






