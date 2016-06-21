#!/usr/bin/python

def sqrt(num):
    result = 0
    shift = 1 << 126
    while (shift > num):
        shift = shift >> 2
    
    while (shift != 0):
        shiftSum = result + shift
        if num >= shiftSum:
            num = num - shiftSum
            result = (result >> 1) + shift
        else:
            result = result >> 1
        shift = shift >> 2
    return result

print sqrt(256)

