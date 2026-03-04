#!/usr/bin/env python3
"""Test Part 2 with the example"""

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

# Process all problems
total = 0
for prob_idx, (start_col, end_col) in enumerate(problems):
    print(f"\nProblem {prob_idx + 1} (columns {start_col} to {end_col}):")
    
    # Build matrix
    matrix = []
    for line in number_lines:
        row = []
        for col in range(start_col, end_col):
            if col < len(line):
                row.append(line[col])
            else:
                row.append(' ')
        matrix.append(row)
    
    # Read columns from right to left
    numbers = []
    for col_idx in range(len(matrix[0]) - 1, -1, -1):
        column = [row[col_idx] for row in matrix]
        has_digits = any(char.isdigit() for char in column)
        if has_digits:
            num_digits = []
            for char in column:
                if char.isdigit():
                    num_digits.append(char)
            if num_digits:
                num_str = ''.join(num_digits)
                numbers.append(int(num_str))
    
    # Get operator
    op_str = operator_line[start_col:end_col] if start_col < len(operator_line) else ''
    operator = None
    if '*' in op_str:
        operator = '*'
    elif '+' in op_str:
        operator = '+'
    
    if not numbers or operator is None:
        continue
    
    # Calculate result
    if operator == '*':
        result = 1
        for num in numbers:
            result *= num
    else:
        result = sum(numbers)
    
    print(f"  Numbers: {numbers}")
    print(f"  Operator: {operator}")
    print(f"  Result: {result}")
    total += result

print(f"\nGrand total: {total} (expected: 3263827)")
