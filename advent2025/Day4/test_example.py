#!/usr/bin/env python3
"""Test with the example from Day 4 Part 1 problem"""

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

print("Example grid:")
for line in example_grid:
    print(line)

print("\nChecking accessible rolls (marked with 'x'):")
accessible_count = 0
result_grid = [list(line) for line in example_grid]

for row in range(len(example_grid)):
    for col in range(len(example_grid[row])):
        if example_grid[row][col] == '@':
            adjacent_rolls = count_adjacent_rolls(example_grid, row, col)
            if adjacent_rolls < 4:
                result_grid[row][col] = 'x'
                accessible_count += 1

print("\nResult (x = accessible):")
for line in result_grid:
    print(''.join(line))

print(f"\nAccessible rolls: {accessible_count} (expected: 13)")






