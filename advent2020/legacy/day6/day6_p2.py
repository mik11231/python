#!/usr/bin/env python
"""
advent2020/legacy/day6/day6_p2.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2020.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""


def sum_answers(input):
    """
    Run `sum_answers` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: input.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    group_sum = 0
    for group in input:
        people = group.split(" ")
        if len(people) == 1:
            group_sum += len(people[0])
        else:
            qa = []
            matches = 0
            # Create unique list of answers as sets
            for person in people:
                for question in person:
                    if set(question) not in qa:
                        qa.append(set(question))
            # Check to see if every person in a group gave a specific
            # answer and add to the total if so
            for answer in qa:
                matches = 0
                for person in people:
                    if answer.issubset(set(person)):
                        matches += 1
                # Only add to total if all people have an anwer
                if matches == len(people):
                    group_sum += 1
    return group_sum


with open("input", "r") as input:
    in_list = input.read().split("\n\n")
    for i in range(len(in_list)):
        in_list[i] = in_list[i].replace("\n", " ")
    # Remove the blank left by last newline
    in_list[-1] = in_list[-1][:len(in_list[-1])-1]

print(sum_answers(in_list))
