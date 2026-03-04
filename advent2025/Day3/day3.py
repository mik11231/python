#!/usr/bin/env python3
"""Advent of Code 2025 - Day 3: Lobby"""

from pathlib import Path
def find_max_joltage(bank):
    """
    Find the maximum joltage possible from a bank by selecting exactly 2 batteries.
    
    Args:
        bank: String of digits representing battery joltages
        
    Returns:
        Maximum 2-digit number that can be formed
    """
    max_joltage = 0
    
    # Try all possible pairs of positions (i, j) where i < j
    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            # Form the 2-digit number from positions i and j
            joltage = int(bank[i]) * 10 + int(bank[j])
            max_joltage = max(max_joltage, joltage)
    
    return max_joltage

def solve():
    """Solve Day 3 Part 1: Find total output joltage."""
    # Read input
    with open(Path(__file__).with_name('d3_input.txt'), 'r') as f:
        banks = [line.strip() for line in f.readlines()]
    
    total_joltage = 0
    
    # Find maximum joltage for each bank
    for bank in banks:
        max_jolt = find_max_joltage(bank)
        total_joltage += max_jolt
    
    return total_joltage

if __name__ == "__main__":
    result = solve()
    print(f"The total output joltage is: {result}")






