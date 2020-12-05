#!/usr/bin/env python

def check_passwords(input_list):
    valid_num = 0
    for password in input_list:
        elements = password.split(' ')
        count = elements[0].split('-')
        pos1 = int(count[0]) - 1
        pos2 = int(count[1]) - 1
        letter = elements[1].strip(':')
        pwd = elements[2]
        # Keep track of count in pwd
        letter_in_pwd = 0
        if pwd[pos1] is letter:
            letter_in_pwd += 1
        if pwd[pos2] is letter:
            letter_in_pwd += 1

        # Only valid if letter in password just recorded once at location
        if letter_in_pwd == 1:
            valid_num += letter_in_pwd

    print(valid_num)
    return


with open("input", "r") as input:
    in_list = input.read().splitlines()

check_passwords(in_list)
