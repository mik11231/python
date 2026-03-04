#!/usr/bin/env python3
"""Advent of Code 2025 - Day 7 Part 2: Laboratories (Quantum Tachyon Manifold)"""

from pathlib import Path
def solve():
    """Solve Day 7 Part 2: Count all timelines a particle can end up in.
    
    In the quantum version, each split creates two timelines. We need to count
    the total number of particles at the final row, where each particle represents
    a different timeline (even if multiple particles end up at the same position).
    """
    # Read input
    with open(Path(__file__).with_name('d7_input.txt'), 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f.readlines()]
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Find starting position (S)
    start_row = -1
    start_col = -1
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 'S':
                start_row = row
                start_col = col
                break
        if start_row != -1:
            break
    
    if start_row == -1:
        print("Error: No starting position S found")
        return 0
    
    # Track count of ways to reach each position: dict[row][col] = count
    # Each particle represents a different timeline (even if at same position)
    position_counts = {start_row: {start_col: 1}}
    
    # Process row by row from top to bottom
    for row in range(start_row, rows):
        if row not in position_counts or not position_counts[row]:
            break
        
        current_positions = position_counts[row]
        next_row = row + 1
        
        if next_row >= rows:
            # All positions at last row are final timelines
            break
        
        # Initialize next row if needed
        if next_row not in position_counts:
            position_counts[next_row] = {}
        
        for col, count in current_positions.items():
            cell_below = grid[next_row][col] if col < len(grid[next_row]) else '.'
            
            if cell_below == '.':
                # Particle continues down
                position_counts[next_row][col] = position_counts[next_row].get(col, 0) + count
            elif cell_below == '^':
                # Particle hits splitter - creates two timelines
                left_col = col - 1
                right_col = col + 1
                if left_col >= 0:
                    position_counts[next_row][left_col] = position_counts[next_row].get(left_col, 0) + count
                if right_col < cols:
                    position_counts[next_row][right_col] = position_counts[next_row].get(right_col, 0) + count
    
    # Count all final timelines
    # Each particle at the final row represents a timeline
    if rows > 0 and (rows - 1) in position_counts:
        timeline_count = sum(position_counts[rows - 1].values())
    else:
        timeline_count = 0
    
    return timeline_count

if __name__ == "__main__":
    result = solve()
    print(f"The particle ends up on {result} different timelines")
