#!/usr/bin/env python3
"""Advent of Code 2025 - Day 1 Part 2: Secret Entrance (Method 0x434C49434B)"""

from pathlib import Path
def count_zero_occurrences_during_rotation(start_pos, direction, distance):
    """
    Count how many distinct times the dial is at position 0 during a rotation.
    This counts positions visited during the rotation, excluding the start position.
    
    For right rotation: we visit positions (start_pos + i) % 100 for i = 0..distance
    For left rotation: we visit positions (start_pos - i) % 100 for i = 0..distance
    We count how many of these (excluding i=0) equal 0.
    """
    count = 0
    
    if direction == 'R':
        # We're at 0 when (start_pos + i) % 100 == 0 for i in [1, distance]
        # This means start_pos + i is a multiple of 100
        # i = 100k - start_pos, and we need 1 <= i <= distance
        # So: ceil((start_pos + 1) / 100) <= k <= floor((start_pos + distance) / 100)
        first_k = (start_pos + 1 + 99) // 100  # Ceiling of (start_pos + 1) / 100
        last_k = (start_pos + distance) // 100  # Floor of (start_pos + distance) / 100
        if first_k <= last_k:
            count = last_k - first_k + 1
    else:  # direction == 'L'
        # We're at 0 when (start_pos - i) % 100 == 0 for i in [1, distance]
        # This means start_pos - i is a multiple of 100
        # i = start_pos - 100k, and we need 1 <= i <= distance
        # So: (start_pos - distance) / 100 <= k <= (start_pos - 1) / 100
        first_k = (start_pos - distance + 99) // 100  # Ceiling
        last_k = (start_pos - 1) // 100  # Floor
        if first_k <= last_k:
            count = last_k - first_k + 1
    
    return count

def solve_part2():
    """Solve Day 1 Part 2: Count all times dial points at 0 (during and after rotations)."""
    # Read input
    with open(Path(__file__).with_name('d1_input.txt'), 'r') as f:
        rotations = [line.strip() for line in f.readlines()]
    
    # Dial starts at 50
    position = 50
    count = 0
    
    # Count starting position if it's 0
    if position == 0:
        count += 1
    
    # Process each rotation
    for rotation in rotations:
        direction = rotation[0]  # L or R
        distance = int(rotation[1:])  # The number part
        
        # Count times dial is at 0 during the rotation (positions visited, excluding start)
        # This includes the end position if it's 0
        zeros_during = count_zero_occurrences_during_rotation(position, direction, distance)
        count += zeros_during
        
        # Apply rotation
        if direction == 'L':
            position = (position - distance) % 100
        else:  # direction == 'R'
            position = (position + distance) % 100
        
        # Note: We don't need to check if position == 0 here because
        # count_zero_occurrences_during_rotation already counts the end position
    
    return count


def solve():
    """Compatibility wrapper matching the common `solve()` entrypoint."""
    return solve_part2()

if __name__ == "__main__":
    result = solve()
    print(f"The password (method 0x434C49434B) is: {result}")
