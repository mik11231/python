#!/usr/bin/env python
"""
advent2022/legacy/day1/calories.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2022.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""


with open("input") as input:
    elves = []
    total_calories = 0
    for line in input.readlines():
        line = line.rstrip()
        if line != "":
            total_calories += int(line)
        else:
            elves.append(total_calories)
            total_calories = 0

    if total_calories != 0:
        elves.append(total_calories)

print("Max calories elf: " + str(max(elves)))

sorted_elves = sorted(elves)
num_elves = 3
total_calories = 0
while num_elves > 0:
    total_calories += sorted_elves[-num_elves]
    num_elves -= 1

print("Max calories triple elves: " + str(total_calories))
