#!/usr/bin/env python

def find_seat(input):
    id_list = sorted(input)
    missing_id = [id for id in range(id_list[0], id_list[-1]+1)
                  if id not in id_list]
    return missing_id[0]


with open("input", "r") as input:
    in_list = input.read().splitlines()
    seat = []
    for i in range(len(in_list)):
        row = in_list[i][0:7].replace("F", "0").replace("B", "1")
        column = in_list[i][7:10].replace("R", "1").replace("L", "0")
        seat_id = int(row, 2) * 8 + int(column, 2)
        in_list[i] = seat_id

print(find_seat(in_list))
