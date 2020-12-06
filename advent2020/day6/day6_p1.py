#!/usr/bin/env python

def sum_answers(input):
    sum = 0
    for group in input:
        sum += len(set(group))
    return sum


with open("input", "r") as input:
    in_list = input.read().split("\n\n")
    for i in range(len(in_list)):
        in_list[i] = in_list[i].replace("\n", " ").replace(" ", "")

print(sum_answers(in_list))
