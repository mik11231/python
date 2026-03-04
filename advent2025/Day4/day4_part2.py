#!/usr/bin/env python3
"""Advent of Code 2025 - Day 4 Part 2: Printing Department"""

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
    """Solve Day 4 Part 2: Count total rolls that can be removed iteratively."""
    # Read input
    with open(Path(__file__).with_name('d4_input.txt'), 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]
    
    total_removed = 0
    
    # Keep removing rolls until no more can be removed
    while True:
        # Find all accessible rolls in the current state
        accessible_positions = []
        
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                # Only check positions with rolls of paper
                if grid[row][col] == '@':
                    # Count adjacent rolls
                    adjacent_rolls = count_adjacent_rolls(grid, row, col)
                    
                    # If fewer than 4 adjacent rolls, it's accessible
                    if adjacent_rolls < 4:
                        accessible_positions.append((row, col))
        
        # If no accessible rolls, we're done
        if not accessible_positions:
            break
        
        # Remove all accessible rolls
        for row, col in accessible_positions:
            grid[row][col] = '.'  # Remove the roll
            total_removed += 1
    
    return total_removed

if __name__ == "__main__":
    result = solve()
    print(f"The total number of rolls that can be removed is: {result}")






