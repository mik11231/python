"""
advent2018/legacy/advent_d2.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2018.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

# Advent of code day 2
puzzle = open("puzzle_input_day2_serge", "r")
if puzzle.mode is 'r':
    contents = puzzle.readlines()

double_count = 0
triple_count = 0

for line in contents:
    # print(line)
    count = {}
    for char in line:
        if char in count:
            count[char] += 1
        else:
            count[char] = 1

    count_dubs = False
    count_trips = False
    for key in count:
        if count[key] == 2:
            count_dubs = True
            # print key, count[key]
        if count[key] == 3:
            count_trips = True
            # print key, count[key]

    if count_dubs:
        double_count += 1

    if count_trips:
        triple_count += 1

# print(double_count, triple_count)
print(double_count * triple_count)


# part 2
def test_strings(s1, s2):
    """
    Run `test_strings` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s1, s2.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    pos = -1
    for i, (s1c, s2c) in enumerate(zip(s1, s2)):
        if s1c != s2c:
            if pos != -1:
                return False
            else:
                pos = i
    return pos


for string1 in contents:
    for string2 in contents:
        if string1 != string2:
            position = test_strings(string1, string2)
            if position:
                # print(string1 + string2)
                print(string1[:position] + string1[position+1:])
                exit()
