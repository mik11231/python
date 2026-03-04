#!/usr/bin/env python3
"""Advent of Code 2025 - Day 2: Gift Shop"""

from pathlib import Path
def is_invalid_id(product_id):
    """
    Check if a product ID is invalid.
    An invalid ID is made only of some sequence of digits repeated twice.
    Examples: 55 (5 twice), 6464 (64 twice), 123123 (123 twice)
    """
    # Convert to string to check digits
    id_str = str(product_id)
    num_digits = len(id_str)
    
    # Must have even number of digits
    if num_digits % 2 != 0:
        return False
    
    # Split in half and check if both halves are identical
    half_length = num_digits // 2
    first_half = id_str[:half_length]
    second_half = id_str[half_length:]
    
    return first_half == second_half

def solve():
    """Solve Day 2 Part 1: Find and sum all invalid product IDs."""
    # Read input
    with open(Path(__file__).with_name('d2_input.txt'), 'r') as f:
        input_line = f.read().strip()
    
    # Parse ranges
    ranges = []
    for range_str in input_line.split(','):
        if '-' in range_str:
            start, end = map(int, range_str.split('-'))
            ranges.append((start, end))
    
    # Find all invalid IDs
    invalid_ids = []
    
    for start, end in ranges:
        for product_id in range(start, end + 1):
            if is_invalid_id(product_id):
                invalid_ids.append(product_id)
    
    # Sum all invalid IDs
    total = sum(invalid_ids)
    
    return total

if __name__ == "__main__":
    result = solve()
    print(f"The sum of all invalid IDs is: {result}")






