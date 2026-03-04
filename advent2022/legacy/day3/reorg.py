#!/usr/bin/env python
"""
advent2022/legacy/day3/reorg.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2022.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

import string


def item_value(input):
    """
    Run `item_value` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: input.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    items = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    values = {}
    values = {item: i + 1 for i, item in enumerate(items)}
    return values[input]


def same_item(input):
    """
    Run `same_item` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: input.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    bag1 = input[0]
    bag2 = input[1]
    bag3 = input[2]
    for item in bag1:
        if item in bag2 and item in bag3:
            return item


with open("input") as input:
    sum = 0
    num_bags = 0
    groups = []
    group = []
    for line in input.readlines():
        if num_bags == 3:
            groups.append(group)
            num_bags = 0
            group = []
        line = line.rstrip()

        group.append(line)
        num_bags += 1

        split = int(len(line)/2)
        first = line[:split]
        second = line[split:]

        common_item = ""
        for item in first:
            if item in second:
                common_item = item

        sum += item_value(common_item)

    if num_bags == 3:
        groups.append(group)

    print("Priorities for common item: " + str(sum))

    badge_priority = 0
    for group in groups:
        badge_priority += item_value(same_item(group))

    print("Priorities for badges: " + str(badge_priority))
