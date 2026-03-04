#!/usr/bin/env python3
"""Advent of Code 2025 - Day 4: Printing Department"""

from pathlib import Path
def count_adjacent_rolls(grid, row, col):
    """
    Count the number of rolls of paper (@) in the 8 adjacent positions.
    
    Args:
        grid: 2D list of characters
        row: Row index
        col: Column index
        
    Returns:
        Number of adjacent rolls
    """
    count = 0
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Check all 8 adjacent positions
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the current position itself
            
            new_row = row + dr
            new_col = col + dc
            
            # Check if position is within bounds
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if grid[new_row][new_col] == '@':
                    count += 1
    
    return count

def solve():
    """Solve Day 4 Part 1: Count accessible rolls of paper."""
    # Read input
    with open(Path(__file__).with_name('d4_input.txt'), 'r') as f:
        grid = [line.strip() for line in f.readlines()]
    
    accessible_count = 0
    
    # Check each position in the grid
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # Only check positions with rolls of paper
            if grid[row][col] == '@':
                # Count adjacent rolls
                adjacent_rolls = count_adjacent_rolls(grid, row, col)
                
                # If fewer than 4 adjacent rolls, it's accessible
                if adjacent_rolls < 4:
                    accessible_count += 1
    
    return accessible_count

if __name__ == "__main__":
    result = solve()
    print(f"The number of accessible rolls of paper is: {result}")






