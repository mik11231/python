#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_objects` -- Objects in Python
=========================================

LAB Objects Learning Objective: Explore objects in Python and how everything in
                                Python is an object.

a. Fill in the series of functions below that determine the characteristics of
   an object.

b. Write a print_object_flags function that uses the is_* functions to find the
   characteristics of the passed in object and print the characteristics
   (flags).

"""


def is_callable(obj):
    """ returns True if the object is callable """
    # __call__
    if '__call__' in dir(obj):
        return True
    else:
        return False


def is_with(obj):
    """ returns True if the object can be used in a "with" context """
    # __enter__, __exit__
    if '__enter__' in dir(obj) and '__exit__' in dir(obj):
        return True
    else:
        return False


def is_math(obj):
    """ returns True if the object supports +, -, /, and * """
    # __add__, ...
    math_attrs = ['__add__', '__sub__', '__mul__', '__truediv__']
    if set(math_attrs) < set(dir(obj)):
        return True
    else:
        return False


def is_iterable(obj):
    """ returns True if the object is iterable """
    # __iter__
    if '__iter__' in dir(obj):
        return True
    else:
        return False


def print_object_flags(obj):
    """ assess the object for various characteristics and print them """
    print("Current object is: " + str(obj))
    print("Is the object callable: " + str(is_callable(obj)))
    print("Can object be used in \"with\" context: " + str(is_with(obj)))
    print("Does object support math: " + str(is_math(obj)))
    print("Is object iterable: " + str(is_iterable(obj)))
    print("\n")


if __name__ == "__main__":
    print_object_flags(1)
    print_object_flags("abc")
    print_object_flags(print_object_flags)
    print_object_flags([1, 2, 3])
    print_object_flags(open('test.file.deleteme', 'w'))
