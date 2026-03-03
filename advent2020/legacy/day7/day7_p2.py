#!/usr/bin/env python

class Bag():
    def __init__(self, name="Default", contents=[], count=0, definition=False):
        self.name = name
        self.definition = definition
        self.count = count
        self.contents = contents

    def show_counts(self):
        bag_counts = []
        if self.contents:
            for bag in self.contents:
                bag_counts.append([bag.name, bag.contents])
        else:
            bag_counts = None
        return bag_counts


def find_bags(input):
    for bag in input:
        if bag.name == "shiny gold":
            find_count(bag, input)


def find_count(bag, input):
    inside_bags = bag.show_counts()
    # if bag.show_counts():
        # for inside in



# def dig(bag):
#     my_bags = []
#     for item in bag:
#         # print(bag)
#         my_bags += bag[item]
#     return my_bags
    # bag_search = trim(my_bags, input)
    # bag_mountain = []
    # while bag_search[1]:
    #     bag_mountain.append(bag_search[2])
    #     my_bags = bag_search[1]
    #     bag_search = trim(my_bags, bag_search[0])
    #
    # # import json
    # # print(json.dumps(bag_mountain, indent=3))
    # # exit()
    #
    # bag_count = 0
    # down_climb = range(len(bag_mountain)-1, 0, -1)
    #
    # for i in down_climb:
    #     # print(bag_mountain[i], "Current")
    #     # print(bag_mountain[i-1], "Next")
    #     for j in range(len(bag_mountain[i-1])):
    #         bag = bag_mountain[i-1][j]
    #         bag_name = bag.keys()[0]
    #         total_in_count = 0
    #         print(bag_mountain[i])
    #         print(bag)
    #         for inside in bag.values()[0]:
    #             in_count = 0
    #             cur_inside = inside.keys()[0]
    #             cur_count = int(inside.values()[0])
    #             total_in_count += cur_count
    #
    #             for in_bag in bag_mountain[i]:
    #                 if cur_inside in in_bag:
    #                     local_count = 0
    #                     if isinstance(in_bag.values()[0], list):
    #                         for item in in_bag.values()[0]:
    #                             local_count += int(item.values()[0])
    #                     else:
    #                         local_count = in_bag.values()[0]
    #                     # print(local_count, cur_count, "Counts")
    #                     in_count = local_count * cur_count
    #                     # print(in_count, "In Count")
    #                     # print(cur_count, "Cur Count")
    #                     total_in_count += in_count
    #
    #             bag_count = total_in_count
    #             bag_mountain[i-1][j][bag_name] = bag_count
    #         print(bag, "Inside")
    #     print(bag_mountain[i-1], "Outside")
    # return bag_count


# def trim(search_bags, input):
#     valid_bags = []
#     remove_bags = []
#     empty_bags = []
#     bag_pile = []
#     for my_bag in search_bags:
#
#         for i in range(len(input)):
#             if my_bag in input[i]:
#                 if i not in remove_bags:
#                     remove_bags.append(i)
#                 if input[i][my_bag] != ['']:
#                     bag_pile.append(input[i])
#                     for bag in input[i][my_bag]:
#                         valid_bags.append(bag.keys()[0])
#                 else:
#                     if i not in empty_bags and i not in remove_bags:
#                         empty_bags.append(i)
#
#     if empty_bags:
#         remove_bags = sorted(remove_bags + empty_bags)
#     remove_indexes = sorted(remove_bags)
#     for index in reversed(sorted(remove_indexes)):
#         input.pop(index)
#     return [input, valid_bags, bag_pile]


with open("example_input", "r") as input:
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
                inside_bag = Bag(key, inside_items[0])
                bag_contents[j] = inside_bag

        if bag_contents == ['']:
            bag = Bag(bag_details[0][:-1], None, True)
        else:
            bag = Bag(bag_details[0][:-1], bag_contents, True)
        bags.append(bag)

print(find_bags(bags), "Result")
