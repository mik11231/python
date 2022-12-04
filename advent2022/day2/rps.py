#!/usr/bin/env python


def eval(round):
    opponent = {"A": "X", "B": "Y", "C": "Z"}

    if opponent[round[0]] == round[2]:
        return 3
    elif opponent[round[0]] == "X":
        if round[2] == "Y":
            return 6
        else:
            return 0
    elif opponent[round[0]] == "Y":
        if round[2] == "Z":
            return 6
        else:
            return 0
    elif opponent[round[0]] == "Z":
        if round[2] == "X":
            return 6
        else:
            return 0


def resolve(round):
    if round[2] == "X":
        if round[0] == "A":
            return 3
        elif round[0] == "B":
            return 1
        else:
            return 2
    elif round[2] == "Y":
        if round[0] == "A":
            return 1
        elif round[0] == "B":
            return 2
        else:
            return 3
    else:
        if round[0] == "A":
            return 2
        elif round[0] == "B":
            return 3
        else:
            return 1


with open("input") as input:
    first_score = 0
    second_score = 0
    values = {}
    win = {}
    values["X"] = 1
    values["Y"] = 2
    values["Z"] = 3
    win["X"] = 0
    win["Y"] = 3
    win["Z"] = 6
    for line in input.readlines():
        line = line.rstrip()
        if line:
            value = eval(line) + values[line[2]]
            first_score += value

        if line:
            value = resolve(line) + win[line[2]]
            second_score += value

print("First strategy score: " + str(first_score))
print("Second strategy score: " + str(second_score))
