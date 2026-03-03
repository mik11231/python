#!/usr/bin/env python

def validate_passport(pas_list):
    valid_passport = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    valid_passport_count = 0
    for passport in pas_list:
        if valid_passport.issubset(passport.keys()):
            valid_passport_count += 1
    return valid_passport_count


with open("input", "r") as input:
    in_list = input.read().split("\n\n")
    for i in range(len(in_list)):
        in_list[i] = in_list[i].replace("\n", " ")
        passport_dict = {}
        for element in in_list[i].split(" "):
            passport_data = element.split(":")
            if len(passport_data) == 2:
                passport_dict[passport_data[0]] = passport_data[1]
        in_list[i] = passport_dict

print(validate_passport(in_list))
