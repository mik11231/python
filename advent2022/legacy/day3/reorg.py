#!/usr/bin/env python
import string


def item_value(input):
    items = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    values = {}
    values = {item: i + 1 for i, item in enumerate(items)}
    return values[input]


def same_item(input):
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
