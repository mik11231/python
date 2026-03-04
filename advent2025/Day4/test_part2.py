#!/usr/bin/env python3
"""Test Part 2 with the example from the problem"""

def count_adjacent_rolls(grid, row, col):
    """
    Run `count_adjacent_rolls` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid, row, col.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    count = 0
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            
            new_row = row + dr
            new_col = col + dc
            
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if grid[new_row][new_col] == '@':
                    count += 1
    
    return count

# Example grid from the problem
example_grid = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@.",
]

# Convert to list of lists for mutability
grid = [list(line) for line in example_grid]

print("Initial state:")
for line in grid:
    print(''.join(line))

total_removed = 0
iteration = 0

# Keep removing rolls until no more can be removed
while True:
    iteration += 1
    # Find all accessible rolls in the current state
    accessible_positions = []
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '@':
                adjacent_rolls = count_adjacent_rolls(grid, row, col)
                if adjacent_rolls < 4:
                    accessible_positions.append((row, col))
    
    # If no accessible rolls, we're done
    if not accessible_positions:
        break
    
    # Remove all accessible rolls
    for row, col in accessible_positions:
        grid[row][col] = '.'
        total_removed += 1
    
    print(f"\nAfter iteration {iteration}, removed {len(accessible_positions)} rolls (total: {total_removed}):")
    for line in grid:
        print(''.join(line))

print(f"\nTotal rolls removed: {total_removed} (expected: 43)")






