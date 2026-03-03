#!/usr/bin/env python

with open("input") as input:
    elves = []
    total_calories = 0
    for line in input.readlines():
        line = line.rstrip()
        if line != "":
            total_calories += int(line)
        else:
            elves.append(total_calories)
            total_calories = 0

    if total_calories != 0:
        elves.append(total_calories)

print("Max calories elf: " + str(max(elves)))

sorted_elves = sorted(elves)
num_elves = 3
total_calories = 0
while num_elves > 0:
    total_calories += sorted_elves[-num_elves]
    num_elves -= 1

print("Max calories triple elves: " + str(total_calories))
