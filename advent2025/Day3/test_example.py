#!/usr/bin/env python3
"""Test with the example from Day 3 Part 1 problem"""

def find_max_joltage(bank):
    max_joltage = 0
    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            joltage = int(bank[i]) * 10 + int(bank[j])
            max_joltage = max(max_joltage, joltage)
    return max_joltage

# Test cases from the problem
test_banks = [
    ("987654321111111", 98),   # Should produce 98
    ("811111111111119", 89),   # Should produce 89
    ("234234234234278", 78),   # Should produce 78
    ("818181911112111", 92),   # Should produce 92
]

print("Testing example banks:")
all_passed = True
total = 0
for bank, expected in test_banks:
    result = find_max_joltage(bank)
    total += result
    status = "PASS" if result == expected else "FAIL"
    if result != expected:
        all_passed = False
    print(f"{status} Bank {bank}: expected {expected}, got {result}")

print(f"\nTotal joltage: {total} (expected: 357)")

if all_passed and total == 357:
    print("\nAll tests passed!")
else:
    print("\nSome tests failed!")






