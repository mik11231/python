# day 4 all the things!
from datetime import datetime
puzzle = open("puzzle_input_day4", "r")
if puzzle.mode is 'r':
    contents = puzzle.readlines()
	
time_dict = {}
	
for item in contents:
	date = item[int(item.index('[') + 1):int(item.index(']'))]
	action = item[int(item.index(']') + 2):]
	time_dict[date] = action
	
keylist = time_dict.keys()
keylist.sort()
current_gid = 0

for key in keylist:
	try:
		id_index = str(time_dict[key]).index('#')
		b_index = str(time_dict[key]).index('b')
		gid = str(time_dict[key][int(id_index + 1): int(b_index - 1)])
		current_gid = gid
	except Exception:
		space_index = str(time_dict[key]).index(' ')
		min = key[key.index(':') + 1:]
		day = key[key.index(' ') - 5:key.index(' ')]
		string = str(time_dict[key])
		action = string[:space_index]
		# print(current_gid) 
		print(current_gid, day, min, action)
