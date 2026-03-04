#!/usr/bin/env python3
"""Advent of Code 2025 - Day 2 Part 2: Gift Shop"""

from pathlib import Path
def is_invalid_id(product_id):
    """
    Check if a product ID is invalid.
    An invalid ID is made only of some sequence of digits repeated at least twice.
    Examples: 12341234 (1234 two times), 123123123 (123 three times), 
              1212121212 (12 five times), 1111111 (1 seven times)
    """
    # Convert to string to check digits
    id_str = str(product_id)
    num_digits = len(id_str)
    
    # Try all possible pattern lengths from 1 to num_digits // 2
    # (since we need at least 2 repetitions)
    for pattern_length in range(1, num_digits // 2 + 1):
        # Check if the number of digits is divisible by pattern length
        if num_digits % pattern_length != 0:
            continue
        
        # Extract the pattern (first pattern_length digits)
        pattern = id_str[:pattern_length]
        
        # Calculate how many times the pattern should repeat
        num_repetitions = num_digits // pattern_length
        
        # Check if the entire number equals the pattern repeated num_repetitions times
        if id_str == pattern * num_repetitions:
            return True
    
    return False

def solve():
    """Solve Day 2 Part 2: Find and sum all invalid product IDs."""
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






