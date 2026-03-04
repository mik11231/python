#!/usr/bin/env python3
"""Advent of Code 2025 - Day 6 Part 2: Trash Compactor"""

from pathlib import Path
def solve():
    """Solve Day 6 Part 2: Calculate grand total reading right-to-left."""
    # Read input
    with open(Path(__file__).with_name('d6_input.txt'), 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
    
    # Find the operator line (line with * or +)
    operator_line_idx = -1
    for i, line in enumerate(lines):
        if '*' in line or '+' in line:
            operator_line_idx = i
            break
    
    if operator_line_idx == -1:
        print("Error: No operator line found")
        return 0
    
    # Number lines are before the operator line
    number_lines = lines[:operator_line_idx]
    operator_line = lines[operator_line_idx]
    
    # Get maximum line length
    max_len = max(len(line) for line in lines)
    
    # Find problem columns (same as Part 1)
    problems = []
    in_problem = False
    problem_start = None
    
    for col in range(max_len + 1):
        has_content = False
        for line in lines:
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
    
    # Process each problem (read right-to-left)
    total = 0
    
    for start_col, end_col in problems:
        # Extract operator
        op_str = operator_line[start_col:end_col] if start_col < len(operator_line) else ''
        operator = None
        if '*' in op_str:
            operator = '*'
        elif '+' in op_str:
            operator = '+'
        
        if operator is None:
            continue
        
        # Read numbers right-to-left, column by column
        # Each column represents one number, with digits stacked vertically
        # (top = most significant, bottom = least significant)
        
        # Build a matrix of characters for this problem
        problem_matrix = []
        for line in number_lines:
            row = []
            for col in range(start_col, end_col):
                if col < len(line):
                    row.append(line[col])
                else:
                    row.append(' ')
            problem_matrix.append(row)
        
        # Read columns from right to left
        # Each column with digits represents one number
        numbers = []
        
        for col_idx in range(len(problem_matrix[0]) - 1, -1, -1):
            column = [row[col_idx] for row in problem_matrix]
            
            # Check if this column has any digits
            has_digits = any(char.isdigit() for char in column)
            
            if has_digits:
                # This column represents a number
                # Read digits from top to bottom (most significant to least)
                num_digits = []
                for char in column:
                    if char.isdigit():
                        num_digits.append(char)
                
                if num_digits:
                    num_str = ''.join(num_digits)
                    numbers.append(int(num_str))
        
        if not numbers:
            continue
        
        # Calculate result
        if operator == '*':
            result = 1
            for num in numbers:
                result *= num
        else:  # operator == '+'
            result = sum(numbers)
        
        total += result
    
    return total

if __name__ == "__main__":
    result = solve()
    print(f"The grand total is: {result}")

