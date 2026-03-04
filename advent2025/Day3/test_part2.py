#!/usr/bin/env python3
"""Test Part 2 with the example from the problem"""

def find_max_joltage_12(bank):
    if len(bank) < 12:
        return 0
    
    selected_digits = []
    start_pos = 0
    
    for digit_index in range(12):
        end_pos = len(bank) - (12 - digit_index - 1) - 1
        
        max_digit = '0'
        max_pos = start_pos
        for i in range(start_pos, min(end_pos + 1, len(bank))):
            if bank[i] > max_digit:
                max_digit = bank[i]
                max_pos = i
        
        selected_digits.append(max_digit)
        start_pos = max_pos + 1
    
    return int(''.join(selected_digits))

# Test cases from the problem
test_banks = [
    ("987654321111111", 987654321111),   # Should produce 987654321111
    ("811111111111119", 811111111119),   # Should produce 811111111119
    ("234234234234278", 434234234278),   # Should produce 434234234278
    ("818181911112111", 888911112111),   # Should produce 888911112111
]

print("Testing example banks:")
all_passed = True
total = 0
for bank, expected in test_banks:
    result = find_max_joltage_12(bank)
    total += result
    status = "PASS" if result == expected else "FAIL"
    if result != expected:
        all_passed = False
    print(f"{status} Bank {bank}: expected {expected}, got {result}")

print(f"\nTotal joltage: {total} (expected: 3121910778619)")

if all_passed and total == 3121910778619:
    print("\nAll tests passed!")
else:
    print("\nSome tests failed!")






