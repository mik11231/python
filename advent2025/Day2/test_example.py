#!/usr/bin/env python3
"""Test the example from Day 2 Part 1 problem"""

def is_invalid_id(product_id):
    id_str = str(product_id)
    num_digits = len(id_str)
    if num_digits % 2 != 0:
        return False
    half_length = num_digits // 2
    first_half = id_str[:half_length]
    second_half = id_str[half_length:]
    return first_half == second_half

# Test cases from the problem
test_cases = [
    (11, True),   # 11-22 has 11 and 22
    (22, True),
    (99, True),   # 95-115 has 99
    (1010, True),    # 998-1012 has 1010
    (1188511885, True), # 1188511880-1188511890 has 1188511885
    (222222, True),  # 222220-222224 has 222222
    (446446, True),  # 446443-446449 has 446446
    (38593859, True), # 38593856-38593862 has 38593859
    (10, False),  # Should be valid
    (101, False), # Should be valid
    (100, False), # Should be valid
]

print("Testing invalid ID detection:")
all_passed = True
for product_id, expected in test_cases:
    result = is_invalid_id(product_id)
    status = "PASS" if result == expected else "FAIL"
    if result != expected:
        all_passed = False
    print(f"{status} ID {product_id}: expected {expected}, got {result}")

if all_passed:
    print("\nAll tests passed!")
else:
    print("\nSome tests failed!")

# Test the example ranges
example_ranges = [
    (11, 22),
    (95, 115),
    (998, 1012),
    (1188511880, 1188511890),
    (222220, 222224),
    (1698522, 1698528),
    (446443, 446449),
    (38593856, 38593862),
]

print("\nTesting example ranges:")
total = 0
for start, end in example_ranges:
    invalid_in_range = []
    for product_id in range(start, end + 1):
        if is_invalid_id(product_id):
            invalid_in_range.append(product_id)
            total += product_id
    print(f"Range {start}-{end}: {len(invalid_in_range)} invalid IDs: {invalid_in_range}")

print(f"\nTotal sum: {total} (expected: 1227775554)")






