#!/usr/bin/env python3
"""Test Part 2 with the example from the problem"""

def merge_ranges(ranges):
    """
    Run `merge_ranges` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: ranges.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    if not ranges:
        return []
    
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    
    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        
        if current_start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))
    
    return merged

# Example ranges from the problem
example_ranges = [
    (3, 5),
    (10, 14),
    (16, 20),
    (12, 18),
]

print("Original ranges:")
for start, end in example_ranges:
    print(f"  {start}-{end}")

# Merge overlapping ranges
merged = merge_ranges(example_ranges)

print("\nMerged ranges:")
for start, end in merged:
    print(f"  {start}-{end}")

# Count total unique IDs
total = 0
all_ids = set()

for start, end in merged:
    count = end - start + 1
    total += count
    # Also collect IDs to verify
    for i in range(start, end + 1):
        all_ids.add(i)

print(f"\nTotal fresh IDs: {total}")
print(f"Unique IDs: {sorted(all_ids)}")
print(f"Expected: 14 (IDs: 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)")

if total == 14:
    print("\nTest PASSED!")
else:
    print(f"\nTest FAILED! Expected 14, got {total}")






