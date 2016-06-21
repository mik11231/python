#!/usr/bin/python

#Using digit by digit computation implemented in binary
def sqrt(num):
    result = 0
    #support for 128 bit roots can support larger numbers if edited
    #powers of 4 are used which is why using 126 and not 128
    shift = 1 << 126

    #shit down until we've hit a shift value lower
    #than our initial input
    while (shift > num):
        shift = shift >> 2
    
    #keep shifting down to find the root aproximation
    #closest number that multiplied by itself is not higher than
    #our input
    while (shift != 0):
        shiftSum = result + shift
        if num >= shiftSum:
            num = num - shiftSum
            result = (result >> 1) + shift
        else:
            result = result >> 1
        shift = shift >> 2
    return result

#printing things!
print sqrt(256)

