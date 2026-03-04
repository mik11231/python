#!/usr/bin/env python3
"""Advent of Code 2025 - Day 1: Secret Entrance"""

from pathlib import Path
def solve():
    """Solve Day 1 Part 1: Count how many times dial points at 0."""
    # Read input
    with open(Path(__file__).with_name('d1_input.txt'), 'r') as f:
        rotations = [line.strip() for line in f.readlines()]
    
    # Dial starts at 50
    position = 50
    count = 0
    
    # Process each rotation
    for rotation in rotations:
        direction = rotation[0]  # L or R
        distance = int(rotation[1:])  # The number part
        
        # Apply rotation
        if direction == 'L':
            position = (position - distance) % 100
        else:  # direction == 'R'
            position = (position + distance) % 100
        
        # Count if dial points at 0
        if position == 0:
            count += 1
    
    return count

if __name__ == "__main__":
    result = solve()
    print(f"The password is: {result}")

