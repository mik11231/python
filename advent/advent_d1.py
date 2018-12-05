# Advent of code
def repeat(value, dict):
    puzzle = open("puzzle_input_day1", "r")
    if puzzle.mode is 'r':
        contents = puzzle.readlines()

    dict[value] = 1
    for line in contents:
        value = value + int(line)
        if value in dict:
            dict[value] += 1
            print(value)
            exit()
        else:
            dict[value] = 1

    return [value, dict]


init = 0
recurrence = {}
count = 0

while (2 not in recurrence.values()):
    count += 1
    results = repeat(init, recurrence)
    print(count)
    init = results[0]
    recurrence = results[1]
