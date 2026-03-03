# Day 3 all the area things
# pprint not needed for final results but very handy for visualizing!!
# from pprint import pprint

puzzle = open("puzzle_input_day3", "r")
if puzzle.mode is 'r':
    contents = puzzle.readlines()

# object1 = "#1 @ 1,3: 4x4"
# object2 = "#2 @ 3,1: 4x4"
# object3 = "#3 @ 5,5: 2x2"

counter = 0

table = [[0 for y in range(1000)] for x in range(1000)]

for item in contents:
    id = int(item[int(item.index('#') + 1):int(item.index('@') - 1)])
    x = int(item[int(item.index('@') + 2):int(item.index(','))])
    y = int(item[int(item.index(',') + 1):int(item.index(':'))])
    size_x = int(item[int(item.index(':') + 2):int(item.index('x'))])
    size_y = int(item[int(item.index('x') + 1):])
    # print(id)
    # print(x, y)
    # print(size_x, size_y)

    for i in range(size_x):
        for j in range(size_y):
            table[x+i][y+j] += 1

for i in range(1000):
    for j in range(1000):
        if table[i][j] > 1:
            counter += 1

print counter

for item in contents:
    id = int(item[int(item.index('#') + 1):int(item.index('@') - 1)])
    x = int(item[int(item.index('@') + 2):int(item.index(','))])
    y = int(item[int(item.index(',') + 1):int(item.index(':'))])
    size_x = int(item[int(item.index(':') + 2):int(item.index('x'))])
    size_y = int(item[int(item.index('x') + 1):])
    # print(id)
    # print(x, y)
    # print(size_x, size_y)
    unique = True
    for i in range(size_x):
        for j in range(size_y):
            if table[x+i][y+j] > 1:
                unique = False

    if unique:
        print(id)

# pprint(table)
