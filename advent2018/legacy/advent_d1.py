"""
advent2018/legacy/advent_d1.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2018.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

# Advent of code
def repeat(value, dict):
    """
    Run `repeat` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: value, dict.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    puzzle = open("puzzle_input_day1", "r")
    if puzzle.mode is 'r':
        contents = puzzle.readlines()

    dict[value] = 1
    for line in contents:
        value = value + int(line)
        if value in dict:
            dict[value] += 1
            print(value)
            exit()
        else:
            dict[value] = 1

    return [value, dict]


init = 0
recurrence = {}
count = 0

while (2 not in recurrence.values()):
    count += 1
    results = repeat(init, recurrence)
    print(count)
    init = results[0]
    recurrence = results[1]
