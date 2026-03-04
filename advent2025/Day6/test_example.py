#!/usr/bin/env python3
"""Test with the example from Day 6 Part 1 problem"""

import re

# Example from problem
example_lines = [
    "123 328  51 64 ",
    " 45 64  387 23 ",
    "  6 98  215 314",
    "*   +   *   +  ",
]

# Find operator line
operator_line_idx = -1
for i, line in enumerate(example_lines):
    if '*' in line or '+' in line:
        operator_line_idx = i
        break

number_lines = example_lines[:operator_line_idx]
operator_line = example_lines[operator_line_idx]

max_len = max(len(line) for line in example_lines)

# Find problem columns
problems = []
in_problem = False
problem_start = None

for col in range(max_len + 1):
    has_content = False
    for line in example_lines:
        if col < len(line) and line[col] != ' ':
            has_content = True
            break
    
    if has_content:
        if not in_problem:
            problem_start = col
            in_problem = True
    else:
        if in_problem:
            problems.append((problem_start, col))
            in_problem = False

if in_problem:
    problems.append((problem_start, max_len))

print("Problems found:", problems)
print()

total = 0
for idx, (start_col, end_col) in enumerate(problems):
    numbers = []
    for line in number_lines:
        col_str = line[start_col:end_col] if start_col < len(line) else ''
        nums = re.findall(r'\d+', col_str)
        for num_str in nums:
            numbers.append(int(num_str))
    
    op_str = operator_line[start_col:end_col] if start_col < len(operator_line) else ''
    operator = None
    if '*' in op_str:
        operator = '*'
    elif '+' in op_str:
        operator = '+'
    
    if operator == '*':
        result = 1
        for num in numbers:
            result *= num
    else:
        result = sum(numbers)
    
    print(f"Problem {idx+1}: {numbers} {operator} = {result}")
    total += result

print(f"\nTotal: {total} (expected: 4277556)")






