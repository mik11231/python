#!/usr/bin/env python

def highest_id(input):
    id = 0
    for seat in input:
        tmp_id = seat[0] * 8 + seat[1]
        if tmp_id > id:
            id = tmp_id
    return id


with open("input", "r") as input:
    in_list = input.read().splitlines()
    seat = []
    for i in range(len(in_list)):
        row = in_list[i][0:7].replace("F", "0").replace("B", "1")
        column = in_list[i][7:10].replace("R", "1").replace("L", "0")
        seat = [int(row, 2), int(column, 2)]
        in_list[i] = seat

print(highest_id(in_list))
