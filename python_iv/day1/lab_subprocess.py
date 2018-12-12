#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_subprocess` -- subprocess module
============================================

LAB subprocess Learning Objective: Familiarization with subprocess

::

 a. Use the subprocess run function to run "ls -l" and print the output.

 b. Do the same as a), but don't print anything to the screen.

 c. Do the same as a), but run the command "/bogus/command". What happens?

 d. Use subprocess run function to run "du -h" and output stdout to a pipe.
    Read the pipe and print the output.

 e. Create a new function commander() which takes in a list of commands to
    execute (as strings) on the arg list, then runs them sequentially printing
    stdout.

"""
import subprocess

print("a.")
subprocess.run(['ls', '-l'])

print("\nb.")
print("Running: subprocess.run(['ls', '-l'], output=subprocess.DEVNULL)")
subprocess.run(['ls', '-l'], stdout=subprocess.DEVNULL)

print("\nc.")
try:
    subprocess.run(['/bogus/command'])
except Exception as e:
    print(e)

print("\nd.")
du_h = subprocess.run(['du', '-h'], stdout=subprocess.PIPE)
print(du_h.stdout.decode())


def commander(funcs):
    first = True
    for func in funcs:
        if first:
            char = ""
        else:
            char = "\n"
        first = False
        print(char + "Running command < " + str(func) + " >")
        subprocess.run(func, shell=True)


# def commander_popen(funcs):
#     for func in funcs:
#         du_home = subprocess.Popen(func, shell=True, stdout=subprocess.PIPE)


functions = ["ls -al", "df -h", "mount", "fortune", "who", "whoami"]
print("\ne.")
commander(functions)
# print("\ne. Alt")
# commander_popen(['du -sh ~'])
