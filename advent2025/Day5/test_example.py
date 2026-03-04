#!/usr/bin/env python3
"""Test with the example from Day 5 Part 1 problem"""

# Example input
example_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

lines = [line.strip() for line in example_input.split('\n')]

# Parse ranges and IDs
ranges = []
ingredient_ids = []

# Find the blank line separator
blank_line_index = -1
for i, line in enumerate(lines):
    if not line:  # Blank line
        blank_line_index = i
        break

if blank_line_index == -1:
    for line in lines:
        if '-' in line:
            ranges.append(line)
        elif line:
            ingredient_ids.append(line)
else:
    ranges = [line for line in lines[:blank_line_index] if '-' in line]
    ingredient_ids = [line for line in lines[blank_line_index+1:] if line]

print(f"Ranges: {ranges}")
print(f"Ingredient IDs: {ingredient_ids}")

# Parse ranges into (start, end) tuples
range_tuples = []
for range_str in ranges:
    start, end = map(int, range_str.split('-'))
    range_tuples.append((start, end))

print(f"\nRange tuples: {range_tuples}")

# Check each ingredient ID
fresh_count = 0
results = []

for id_str in ingredient_ids:
    ingredient_id = int(id_str)
    
    # Check if ingredient ID falls into any range
    is_fresh = False
    for start, end in range_tuples:
        if start <= ingredient_id <= end:
            is_fresh = True
            break
    
    status = "fresh" if is_fresh else "spoiled"
    results.append((ingredient_id, status))
    if is_fresh:
        fresh_count += 1

print("\nResults:")
for ingredient_id, status in results:
    print(f"Ingredient ID {ingredient_id} is {status}")

print(f"\nTotal fresh: {fresh_count} (expected: 3)")






