#!/usr/bin/env python3
"""Test Day 7 Part 2 with the example from the problem"""

example_grid = [
    ".......S.......",
    "...............",
    ".......^.......",
    "...............",
    "......^.^......",
    "...............",
    ".....^.^.^.....",
    "...............",
    "....^.^...^....",
    "...............",
    "...^.^...^.^...",
    "...............",
    "..^...^.....^..",
    "...............",
    ".^.^.^.^.^...^.",
    "...............",
]

def solve_example():
    """Solve the example and count timelines."""
    grid = [list(line) for line in example_grid]
    
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
    
    print(f"Start position: ({start_row}, {start_col})")
    print(f"Grid size: {rows} rows x {cols} cols")
    
    # Track count of ways to reach each position: dict[row][col] = count
    # This allows us to properly count all timelines
    position_counts = {start_row: {start_col: 1}}
    
    # Process row by row from top to bottom
    for row in range(start_row, rows):
        if row not in position_counts or not position_counts[row]:
            break
        
        current_positions = position_counts[row]
        total_at_row = sum(current_positions.values())
        print(f"\nRow {row}: {len(current_positions)} positions, {total_at_row} total particles: {sorted(current_positions.keys())}")
        
        # Initialize next row if needed
        next_row = row + 1
        if next_row >= rows:
            # All positions at last row are final timelines
            break
        
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
                print(f"  Position ({row}, {col}) with count {count} splits -> adds {count} to ({next_row}, {left_col}) and ({next_row}, {right_col})")
        
        next_total = sum(position_counts[next_row].values())
        print(f"  Next row {next_row} will have {len(position_counts[next_row])} positions, {next_total} total particles: {sorted(position_counts[next_row].keys())}")
    
    # Count all final timelines
    # Each particle at the final row represents a timeline
    if rows > 0 and (rows - 1) in position_counts:
        final_timelines = position_counts[rows - 1]
        timeline_count = sum(final_timelines.values())  # Total particles = total timelines
        unique_positions = len(final_timelines)
        print(f"\nFinal row {rows - 1} has {unique_positions} unique positions: {sorted(final_timelines.keys())}")
        print(f"Total particles at final row: {timeline_count}")
        print(f"Total timelines: {timeline_count}")
    
    print(f"\nTotal timelines: {timeline_count} (expected: 40)")
    return timeline_count

if __name__ == "__main__":
    expected = 40
    actual = solve_example()
    if actual == expected:
        print("\nExample test PASSED!")
    else:
        print(f"\nExample test FAILED! Expected {expected}, got {actual}")

