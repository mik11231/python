#!/usr/bin/python
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("num", type = int, help = "Display the specified number of elements in the fibbonacci sequence. This must be an int")
parser.add_argument("-r", "--recursive", help = "Use the recursive function", action = "store_true")
parser.add_argument("-t", "--time", help = "Time how long it takes", action = "store_true")
args = parser.parse_args()

#Loop Implementation of fibbonacci
def fib_loop(num):
    first = 1
    second = 1
    counter = 0
     
    while (counter < num):
        result = first
        first = second
        print result
        second = result+second
        counter += 1
    return result

#Recursive implementation of fibbonacci and print progress
def fib_recursive(num,first,second):
    if num == 1:
        result = first
        return result
    elif num == 2:
        result = second
    print(first)        
    result = fib_recursive(num - 1, second, first+second) 
    return result

#Initiate recursive function and print final result at the end
def fib_r(num):
    result = fib_recursive(num, 1, 1)
    print result
    return result

###############################
# Pre argparse implementation #
###############################
#Options, the number of fibbonacci numbers to compute, use loop or recursion
#time the function
#fib_num = raw_input("How many fibbonacci numbers would you like displayed: ")
###############################
###############################

#Grab the number from argparse
#fib_num is pre arg-parse
fib_num = args.num

#############################
# Int check before argparse #
#############################
#Check if input was a number and if greater than or equal to 1 else stop
#try:
#	int(fib_num)
#except:
#	print("Must be a number")
#	quit()
#fib_num = int(fib_num)
#############################
#############################

#Check that we're asking for 1 or more elements in the fibbonacci sequence
if (fib_num < 1):
    print("Number must be larger than 0")
    quit()

###############################
# Pre argparse implementation #
###############################
#fib_type = raw_input("Loop(l) or Recursive(r)?: ")
#Check if loop or recursive was requested, default to loop otherwise
#if fib_type != "l" and fib_type != "r":
###############################
###############################

#Check if recursive flag is set or default to loop
#fib_type left over from pre-argparse so setting it in case we want to revert
if args.recursive:
    if fib_num >= 999:
        print("Beyond python recursion limit, specify a number lower than 999 for recursive version")
        quit()
    else:
	    fib_type = "r"
else:
    #print("Defaulting to loop")
    fib_type = "l"

###############################
# Pre argparse implementation #
###############################
#fib_time = raw_input("Time how long it takes(y/n)?: ")
#Check if we want to time the operation, default to no
#if fib_time == ("y" or "yes"):
###############################
###############################

#Check if time flag is set or default to no
#fib_time left over from pre-argparse so setting it in case we want to revert
if args.time:
    fib_time = True
#elif fib_time == ("n" or "no"):
#    fib_time = False
else:
#	print("Defaulting to no")
	fib_time = False

#Once options are set run our functions

if fib_type == "l":
    if fib_time:
        start_time = time.time()
		#Try block which will catch an interrupt instead of giving ugly output
        try:
            fib_loop(fib_num)
        except KeyboardInterrupt:
            print "Interrupted by user"
            print("--- %s seconds ---" % (time.time() - start_time))
            quit()
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        try:
            fib_loop(fib_num)
        except KeyboardInterrupt:
            print "Interrupted by user"
            quit()

elif fib_type == "r":    
    if fib_time:
        start_time = time.time()
		#Use try block to catch interrupt instead of ugly output
        try:
            fib_r(fib_num)
        except KeyboardInterrupt:
            print "Interrupted by user"
            print("--- %s seconds ---" % (time.time() - start_time))
            quit()
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        try:
            fib_r(fib_num)
        except KeyboardInterrupt:
            print "Interrupted by user"
            quit()
