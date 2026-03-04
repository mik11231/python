#!/usr/bin/env python3
"""Advent of Code 2025 - Day 6: Trash Compactor"""

from pathlib import Path
import re

def solve():
    """Solve Day 6 Part 1: Calculate grand total of all problems."""
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
    
    # Find problem columns
    # A problem column is a vertical region with numbers/operators
    # Separated by columns of only spaces (2+ consecutive spaces)
    
    # First, identify all "words" (sequences of non-space chars) and their positions
    problems = []  # List of (start_col, end_col) for each problem
    
    # Scan through columns to find problem boundaries
    in_problem = False
    problem_start = None
    
    for col in range(max_len + 1):
        # Check if this column has any content
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
            # Empty column
            if in_problem:
                # End of current problem
                problems.append((problem_start, col))
                in_problem = False
    
    # Handle case where last problem doesn't end with spaces
    if in_problem:
        problems.append((problem_start, max_len))
    
    # Process each problem
    total = 0
    
    for start_col, end_col in problems:
        # Extract all numbers from this column in number lines
        numbers = []
        for line in number_lines:
            # Get the substring for this column
            col_str = line[start_col:end_col] if start_col < len(line) else ''
            # Find all numbers in this substring
            nums = re.findall(r'\d+', col_str)
            for num_str in nums:
                numbers.append(int(num_str))
        
        # Extract operator from operator line
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
        else:  # operator == '+'
            result = sum(numbers)
        
        total += result
    
    return total

if __name__ == "__main__":
    result = solve()
    print(f"The grand total is: {result}")

