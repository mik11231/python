#!/usr/bin/env python

def fix_expense(input_list):
    # Find the highest number that could be summed to add up to 2020
    highest_num = 2020 - input_list[0] - input_list[1]
    list_size = len(input_list)
    new_list = []
    # Remove all elements from the list that are larger than our largest
    # possible number and give us the remaining list
    for i in range(list_size):
        if input_list[i] > highest_num:
            new_list = input_list[0:i]
            break

    # Triple for loop through our smaller list to find our numbers
    for num1 in new_list:
        for num2 in new_list:
            if num1 != num2:
                for num3 in new_list:
                    if (num1 != num3) and (num2 != num3):
                        sum = num1 + num2 + num3
                        if sum == 2020:
                            print(num1 * num2 * num3)
                            return


with open("input", "r") as input:
    in_list = sorted([int(i) for i in input.read().splitlines()])


fix_expense(in_list)
