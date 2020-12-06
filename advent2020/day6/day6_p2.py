#!/usr/bin/env python

def sum_answers(input):
    group_sum = 0
    for group in input:
        people = group.split(" ")
        if len(people) == 1:
            group_sum += len(people[0])
        else:
            qa = []
            matches = 0
            # Create unique list of answers as sets
            for person in people:
                for question in person:
                    if set(question) not in qa:
                        qa.append(set(question))
            # Check to see if every person in a group gave a specific
            # answer and add to the total if so
            for answer in qa:
                matches = 0
                for person in people:
                    if answer.issubset(set(person)):
                        matches += 1
                # Only add to total if all people have an anwer
                if matches == len(people):
                    group_sum += 1
    return group_sum


with open("input", "r") as input:
    in_list = input.read().split("\n\n")
    for i in range(len(in_list)):
        in_list[i] = in_list[i].replace("\n", " ")
    # Remove the blank left by last newline
    in_list[-1] = in_list[-1][:len(in_list[-1])-1]

print(sum_answers(in_list))
