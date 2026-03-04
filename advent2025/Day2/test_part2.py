#!/usr/bin/env python3
"""Test Part 2 with example cases"""

def is_invalid_id(product_id):
    """
    Run `is_invalid_id` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: product_id.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    id_str = str(product_id)
    num_digits = len(id_str)
    
    for pattern_length in range(1, num_digits // 2 + 1):
        if num_digits % pattern_length != 0:
            continue
        pattern = id_str[:pattern_length]
        num_repetitions = num_digits // pattern_length
        if id_str == pattern * num_repetitions:
            return True
    return False

# Test cases from the problem
test_cases = [
    (11, True),      # 11-22 has 11 and 22
    (22, True),
    (99, True),      # 95-115 has 99
    (111, True),     # 95-115 has 111 (new in part 2)
    (1010, True),    # 998-1012 has 1010
    (999, True),     # 998-1012 has 999 (new in part 2)
    (1188511885, True), # 1188511880-1188511890 has 1188511885
    (222222, True),  # 222220-222224 has 222222
    (446446, True),  # 446443-446449 has 446446
    (38593859, True), # 38593856-38593862 has 38593859
    (565656, True),  # 565653-565659 has 565656 (new in part 2)
    (824824824, True), # 824824821-824824827 has 824824824 (new in part 2)
    (2121212121, True), # 2121212118-2121212124 has 2121212121 (new in part 2)
    (12341234, True), # Example: 1234 two times
    (123123123, True), # Example: 123 three times
    (1212121212, True), # Example: 12 five times
    (1111111, True), # Example: 1 seven times
    (10, False),     # Should be valid
    (101, False),    # Should be valid
    (100, False),    # Should be valid
    (123, False),    # Should be valid
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
    (565653, 565659),
    (824824821, 824824827),
    (2121212118, 2121212124),
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

print(f"\nTotal sum: {total} (expected: 4174379265)")






