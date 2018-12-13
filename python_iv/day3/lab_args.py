#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_args` -- Arguing with the functions
=========================================

LAB_ARGS Learning Objective: Learn to modify, receive, and work with arguments
to function.
::

 a. Create a function that accepts any number of positional arguments and
    keyword arguments and prints the argument values out to the screen.

 b. Create a function that takes in any number of positional arguments, turns
    those arguments into keyword arguments using "arg#" for the keyword names,
    and calls the print function you wrote in a.

 c. Write a validation function that takes in a variable number of positional
    arguments.  Validate that all the arguments passed in are integers and are
    greater than 0.  If the arguments validate, call the print function, if an
    argument doesn't validate raise a ValueError.

"""


def pos_args(*args, **kwargs):
    for arg in args:
        print("This is a positional arg: " + str(arg))
    for kwarg in kwargs.values():
        print("This is a key word arg: " + str(kwarg))


def arg_converter(*args):
    arg_dict = {}
    for pos, arg in enumerate(args):
        key = "arg" + str(pos)
        arg_dict[key] = str(arg)
    pos_args(**arg_dict)


def validate_ints(*args):
    for arg in args:
        try:
            num = int(arg)
        except ValueError:
            raise ValueError("Value not an int")

        if num < 0:
            raise ValueError("Value less than 0")
        print(num)


pos_args("a", "b", "c", arg_converter("d", "e", "f"))
pos_args("g", "h", "i")
arg_converter("j", "k", "l")
validate_ints(1, 2, 3)
