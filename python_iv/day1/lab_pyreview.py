#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

:mod:`lab_pyreview` -- Python review
=========================================

LAB PyReview Learning Objective: Review the topics from the previous courses

a. Load the data from the two dictionary files in the data directory into two
   list objects.  data/dictionary1.txt data/dictionary2.txt
   Print the number of entries in each list of words from the dictionary files.

b. Use sets in Python to merge the two lists of words with no duplications
   (union). Print the number of words in the combined list.

c. Import the random library and use one of the functions to print out five
   random words from the combined list of words.

d. Use a list comprehension to find all the words that start with the letter
   'a'. Print the number of words that begin with the letter 'a'.

e. Create a function called wordcount() with a yield that takes the list of
   all words as an argument and yields a tuple of
   (letter, number_of_words_starting_with_that_letter) with each iteration.

"""
import random

with open("../RU_Python_IV/data/dictionary1.txt", "r") as dictionary1:
    # dict1_text = dictionary1.readlines()
    # dict1_list = list(dict1_text)
    dict1_list = [line.rstrip() for line in dictionary1]

with open("../RU_Python_IV/data/dictionary2.txt", "r") as dictionary2:
    # dict2_text = dictionary2.readlines()
    # dict2_list = list(dict2_text)
    dict2_list = [line.rstrip() for line in dictionary2]

print("Length of dictionary 1: " + str(len(dict1_list)))
print("Length of dictionary 2: " + str(len(dict2_list)))

set1 = set(dict1_list)
set2 = set(dict2_list)

unified_set = set1.union(set2)

print("Length of combined dictionary: " + str(len(unified_set)))

set_list = list(unified_set)

print("Five random words:")
for i in range(1, 6):
    print(random.choice(set_list))

a_words = [word for word in set_list if word[0] == "a"]
print("Words starting with letter a: " + str(len(a_words)))


def wordcount(word_list):
    from string import ascii_lowercase
    for i in ascii_lowercase:
        word_list = [word for word in set_list if word[0] == i]
        word_tup = (i, len(word_list))
        yield word_tup


test = wordcount(set_list)
print("Tuple output:")
for i in test:
    print(i)
