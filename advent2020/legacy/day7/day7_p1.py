#!/usr/bin/env python
"""
advent2020/legacy/day7/day7_p1.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2020.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""


def find_bags(input):
    # print(input)
    """
    Run `find_bags` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: input.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    my_bags = ["shiny gold"]
    held = 0
    bag_search = trim(my_bags, input)
    removed_bags = []
    while bag_search[0] != 0:
        held += bag_search[0]
        removed_bags.extend(bag_search[2])
        my_bags = bag_search[2]
        bag_search = trim(my_bags, bag_search[1])
    # print(removed_bags)
    return held


def trim(search_bags, input):
    """
    Run `trim` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: search_bags, input.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    valid_bags = []
    remove_bags = []
    empty_bags = []
    for my_bag in search_bags:
        for i in range(len(input)):
            for key in input[i]:
                for contained in input[i][key]:
                    if my_bag in contained:
                        # print(my_bag)
                        valid_bags.append(key)
                        if i not in remove_bags:
                            remove_bags.append(i)
                    elif contained == "":
                        if i not in empty_bags:
                            empty_bags.append(i)

    removed = len(remove_bags)
    if empty_bags:
        remove_bags = sorted(remove_bags + empty_bags)
    remove_indexes = sorted(remove_bags)
    for index in reversed(sorted(remove_indexes)):
        input.pop(index)

    return [removed, input, valid_bags]


with open("example_input2", "r") as input:
    in_list = input.read().splitlines()
    bags = []
    for i in range(len(in_list)):
        bag_details = in_list[i].split("bags contain")
        bag_contents = bag_details[1][1:].replace(" bag", "")\
                                         .replace(" bags", "")\
                                         .replace(".", "")\
                                         .replace("no others", "")\
                                         .replace(", ", ",")\
                                         .split(",")
        for j in range(len(bag_contents)):
            inside_items = bag_contents[j].split(" ")
            if len(inside_items) == 3:
                if inside_items[2][-1] == "s":
                    inside_items[2] = inside_items[2][:-1]
                key = inside_items[1] + " " + inside_items[2]
                inside_dict = {key: inside_items[0]}
                bag_contents[j] = inside_dict

        bag = {bag_details[0][:-1]: bag_contents}
        my_bag = "shiny gold"
        if my_bag in bag:
            continue
        bags.append(bag)


print(find_bags(bags))
