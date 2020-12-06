#!/usr/bin/env python

def validate_passport(pas_list):
    valid_passport = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    valid_passport_count = 0
    for passport in pas_list:
        if valid_passport.issubset(passport.keys()):
            if not validate_byr(passport["byr"]):
                continue
            if not validate_iyr(passport["iyr"]):
                continue
            if not validate_eyr(passport["eyr"]):
                continue
            if not validate_hgt(passport["hgt"]):
                continue
            if not validate_hcl(passport["hcl"]):
                continue
            if not validate_ecl(passport["ecl"]):
                continue
            if not validate_pid(passport["pid"]):
                continue
            valid_passport_count += 1
    return valid_passport_count


def check_range(num, least, most):
    try:
        num = int(num)
        if (num >= least) and (num <= most):
            return True
        else:
            return False
    except Exception:
        return False


def validate_byr(byr):
    return check_range(byr, 1920, 2002)


def validate_iyr(iyr):
    return check_range(iyr, 2010, 2020)


def validate_eyr(eyr):
    return check_range(eyr, 2020, 2030)


def validate_hgt(hgt):
    if "cm" in hgt:
        height = hgt.strip("cm")
        return check_range(height, 150, 193)
    elif "in" in hgt:
        height = hgt.strip("in")
        return check_range(height, 59, 76)
    else:
        return False


def validate_hcl(hcl):
    if (hcl[0] == "#") and (len(hcl) == 7):
        color = hcl.strip("#")
        try:
            int(color, 16)
            return True
        except ValueError:
            return False
    else:
        return False


def validate_ecl(ecl):
    valid_colors = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    color = set([ecl])
    return color.issubset(valid_colors)


def validate_pid(pid):
    if (len(pid) == 9) and pid.isdigit():
        return True
    else:
        return False


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
