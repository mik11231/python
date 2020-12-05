#!/usr/bin/env python

def fix_expense(input_list):
    for first_num in input_list:
        for second_num in input_list:
            sum = int(first_num) + int(second_num)
            if sum == 2020:
                print(int(first_num) * int(second_num))
                return


with open("input", "r") as input:
    in_list = input.read().splitlines()


fix_expense(in_list)
