#!/usr/bin/env python3
"""Tests for Day 4 using the examples from the problem statement.

Part 1 example (4 passports) -> 2 have all required fields.
Part 2 has explicit sets of invalid and valid passports (4 each).
"""

from day4 import parse_passports, has_required_fields
from day4_part2 import is_fully_valid

EXAMPLE_INPUT = """\
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

INVALID_PASSPORTS = """\
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""

VALID_PASSPORTS = """\
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""


def test_part1():
    """Verify Part 1: 2 passports have all required fields."""
    passports = parse_passports(EXAMPLE_INPUT)
    results = [has_required_fields(p) for p in passports]
    assert results == [True, False, True, False], f"Expected [T,F,T,F], got {results}"
    assert sum(results) == 2
    print(f"PASS  Part 1: {sum(results)} valid passports")


def test_part2_invalid():
    """Verify Part 2: all invalid passports are rejected."""
    passports = parse_passports(INVALID_PASSPORTS)
    for i, p in enumerate(passports):
        assert not is_fully_valid(p), f"Passport {i} should be invalid: {p}"
    print(f"PASS  Part 2: all {len(passports)} invalid passports rejected")


def test_part2_valid():
    """Verify Part 2: all valid passports are accepted."""
    passports = parse_passports(VALID_PASSPORTS)
    for i, p in enumerate(passports):
        assert is_fully_valid(p), f"Passport {i} should be valid: {p}"
    print(f"PASS  Part 2: all {len(passports)} valid passports accepted")


if __name__ == "__main__":
    test_part1()
    test_part2_invalid()
    test_part2_valid()
    print("\nAll Day 4 tests passed!")
