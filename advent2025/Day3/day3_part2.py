#!/usr/bin/env python3
"""Advent of Code 2025 - Day 3 Part 2: Lobby"""

from pathlib import Path
def find_max_joltage_12(bank):
    """
    Find the maximum joltage possible from a bank by selecting exactly 12 batteries.
    
    Uses a greedy algorithm: at each position, pick the largest digit available
    while ensuring we can still pick enough digits to reach 12 total.
    
    Args:
        bank: String of digits representing battery joltages
        
    Returns:
        Maximum 12-digit number that can be formed
    """
    if len(bank) < 12:
        # Not enough batteries, return 0 or handle error
        return 0
    
    selected_digits = []
    start_pos = 0
    
    # We need to select 12 digits
    for digit_index in range(12):
        # For the (digit_index+1)-th digit, we need (12 - digit_index - 1) more digits after it
        # So we can only pick from positions where there are enough remaining positions
        end_pos = len(bank) - (12 - digit_index - 1) - 1
        
        # Find the maximum digit in the available range
        max_digit = '0'
        max_pos = start_pos
        for i in range(start_pos, min(end_pos + 1, len(bank))):
            if bank[i] > max_digit:
                max_digit = bank[i]
                max_pos = i
        
        # Select this digit and move the start position forward
        selected_digits.append(max_digit)
        start_pos = max_pos + 1
    
    # Form the number from selected digits
    return int(''.join(selected_digits))

def solve():
    """Solve Day 3 Part 2: Find total output joltage with 12 batteries per bank."""
    # Read input
    with open(Path(__file__).with_name('d3_input.txt'), 'r') as f:
        banks = [line.strip() for line in f.readlines()]
    
    total_joltage = 0
    
    # Find maximum joltage for each bank
    for bank in banks:
        max_jolt = find_max_joltage_12(bank)
        total_joltage += max_jolt
    
    return total_joltage

if __name__ == "__main__":
    result = solve()
    print(f"The total output joltage is: {result}")

