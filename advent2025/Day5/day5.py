#!/usr/bin/env python3
"""Advent of Code 2025 - Day 5: Cafeteria"""

from pathlib import Path
def solve():
    """Solve Day 5 Part 1: Count fresh ingredient IDs."""
    # Read input
    with open(Path(__file__).with_name('d5_input.txt'), 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    # Parse ranges and IDs
    ranges = []
    ingredient_ids = []
    
    # Find the blank line separator
    blank_line_index = -1
    for i, line in enumerate(lines):
        if not line:  # Blank line
            blank_line_index = i
            break
    
    if blank_line_index == -1:
        # If no blank line, assume all lines with '-' are ranges, rest are IDs
        for line in lines:
            if '-' in line:
                ranges.append(line)
            elif line:  # Skip empty lines
                ingredient_ids.append(line)
    else:
        # Split at blank line
        ranges = [line for line in lines[:blank_line_index] if '-' in line]
        ingredient_ids = [line for line in lines[blank_line_index+1:] if line]
    
    # Parse ranges into (start, end) tuples
    range_tuples = []
    for range_str in ranges:
        start, end = map(int, range_str.split('-'))
        range_tuples.append((start, end))
    
    # Check each ingredient ID
    fresh_count = 0
    
    for id_str in ingredient_ids:
        ingredient_id = int(id_str)
        
        # Check if ingredient ID falls into any range
        is_fresh = False
        for start, end in range_tuples:
            if start <= ingredient_id <= end:
                is_fresh = True
                break
        
        if is_fresh:
            fresh_count += 1
    
    return fresh_count

if __name__ == "__main__":
    result = solve()
    print(f"The number of fresh ingredient IDs is: {result}")






