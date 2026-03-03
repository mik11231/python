#!/usr/bin/env python

def check_passwords(input_list):
    valid_num = 0
    for password in input_list:
        elements = password.split(' ')
        count = elements[0].split('-')
        count_min = int(count[0])
        count_max = int(count[1])
        letter = elements[1].strip(':')
        pwd = elements[2]
        occurence = len(pwd.split(letter)) - 1
        if (occurence >= count_min) and (occurence <= count_max):
            valid_num += 1
    print(valid_num)
    return


with open("input", "r") as input:
    in_list = input.read().splitlines()

check_passwords(in_list)
