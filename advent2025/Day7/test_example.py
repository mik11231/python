#!/usr/bin/env python3
"""Test Day 7 Part 1 with the example from the problem"""

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
    """Solve the example and count splits."""
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
    
    # Track active beams: set of (row, col) positions
    active_beams = {(start_row, start_col)}
    split_count = 0
    
    # Process row by row from top to bottom
    for row in range(start_row, rows):
        # Get all beams at this row
        current_beams = {beam for beam in active_beams if beam[0] == row}
        
        if not current_beams:
            # No more active beams
            break
        
        print(f"\nRow {row}: {len(current_beams)} active beams at positions {current_beams}")
        
        # Remove current row beams (they're moving down)
        active_beams -= current_beams
        
        # Process each beam at this row
        new_beams = set()
        
        for beam_row, beam_col in current_beams:
            # Check what's below this beam
            next_row = beam_row + 1
            
            if next_row >= rows:
                # Beam exits the grid
                continue
            
            # Check the cell directly below
            cell_below = grid[next_row][beam_col] if beam_col < len(grid[next_row]) else '.'
            
            print(f"  Beam at ({beam_row}, {beam_col}) -> cell below ({next_row}, {beam_col}) = '{cell_below}'")
            
            if cell_below == '.':
                # Beam continues straight down
                new_beams.add((next_row, beam_col))
            elif cell_below == '^':
                # Beam hits a splitter - split into left and right
                split_count += 1
                print(f"    SPLIT #{split_count} at ({next_row}, {beam_col})")
                
                # Create beam to the left
                left_col = beam_col - 1
                if left_col >= 0:
                    new_beams.add((next_row, left_col))
                    print(f"      New beam at ({next_row}, {left_col})")
                
                # Create beam to the right
                right_col = beam_col + 1
                if right_col < cols:
                    new_beams.add((next_row, right_col))
                    print(f"      New beam at ({next_row}, {right_col})")
        
        # Add new beams (using set to avoid duplicates if multiple beams hit same splitter)
        active_beams.update(new_beams)
        print(f"  New active beams: {active_beams}")
    
    print(f"\nTotal splits: {split_count} (expected: 21)")
    return split_count

if __name__ == "__main__":
    expected = 21
    actual = solve_example()
    if actual == expected:
        print("\nExample test PASSED!")
    else:
        print(f"\nExample test FAILED! Expected {expected}, got {actual}")





