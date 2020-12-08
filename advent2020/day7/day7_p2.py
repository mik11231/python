#!/usr/bin/env python

def find_bags(input):
    my_bags = ["shiny gold"]
    count = 0
    bag_search = trim(my_bags, input)
    removed_bags = []
    while bag_search[0]:
        tmp_count = count
        for multiplier in bag_search[0]:
            count += (tmp_count * multiplier)
        removed_bags.extend(bag_search[2])
        my_bags = bag_search[2]
        bag_search = trim(my_bags, bag_search[1])
    print(removed_bags)
    return count


def trim(search_bags, input):
    valid_bags = []
    remove_bags = []
    empty_bags = []
    count = []
    for my_bag in search_bags:
        for i in range(len(input)):
            for key in input[i]:
                for contained in input[i][key]:
                    print(contained)
                    if my_bag in input[i][key]:
                        print(my_bag)
                        valid_bags.append(key)
                        count.append(input[i][my_bag])
                        if i not in remove_bags:
                            remove_bags.append(i)
                    elif contained == "":
                        if i not in empty_bags:
                            empty_bags.append(i)

    print(count)
    if empty_bags:
        remove_bags = sorted(remove_bags + empty_bags)
    remove_indexes = sorted(remove_bags)
    for index in reversed(sorted(remove_indexes)):
        input.pop(index)

    return [count, input, valid_bags]


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
        bags.append(bag)


print(find_bags(bags))
