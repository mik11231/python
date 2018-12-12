#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_multi` -- Investigate multiprocessing / multithreading
=========================================

LAB_multi Learning Objective: Learn to use the multiprocessing and
                              multithreading modules to perform parallel tasks.
::

 a. Create set of three functions that perform the following tasks:
    1. Capitalize all strings that come through and pass them along
    2. Count the number of characters in the string and pass along the string
       and the count as a tuple (string, count).
    3. Check to see if the count is the largest seen so far.  If so, send along
       a tuple with (string, count, True), else send (string, count, False)

 b. Spawn each of those functions into processes (multiprocessing) and wire
    them togethe with interprocess communications (queues).

 c. Run the entire data/dictionary2.txt file through your processing engine,
    one word at a time.

 d. In the main process, monitor the results coming from the last stage in the
    processing engine. After all the words have been processed, print the
    longest word that went through the engine.

 e. If you complete the above tasks, go back and do the same tasks using
    threads (threading).  Don't delete your multiprocessing code, just add the
    threading code.

"""
import multiprocessing
import queue
import threading
import time


def capit(q1, q2):
    while True:
        word = q1.get()
        cap_word = word.upper()
        q2.put(cap_word)
        q1.task_done()


def count(q2, q3):
    while True:
        word = q2.get()
        tup = (word, len(word))
        q3.put(tup)
        q2.task_done()


def largest(q3, q4):
    ll = 0
    while True:
        (word, size) = q3.get()
        if size > ll:
            ll = size
            lw = [word, size, True]
            q4.put(lw)
        else:
            sw = [word, size, False]
            q4.put(sw)
        q3.task_done()


if __name__ == "__main__":
    with open("../RU_Python_IV/data/dictionary2.txt", "r") as dictionary2:
        dict2_list = [line.rstrip() for line in dictionary2]

    q1 = multiprocessing.JoinableQueue()
    q2 = multiprocessing.JoinableQueue()
    q3 = multiprocessing.JoinableQueue()
    q4 = multiprocessing.JoinableQueue()

    qt1 = queue.Queue()
    qt2 = queue.Queue()
    qt3 = queue.Queue()
    qt4 = queue.Queue()

    p1 = multiprocessing.Process(target=capit, args=[q1, q2])
    p2 = multiprocessing.Process(target=count, args=[q2, q3])
    p3 = multiprocessing.Process(target=largest, args=[q3, q4])

    t1 = threading.Thread(target=capit, args=[qt1, qt2])
    t2 = threading.Thread(target=count, args=[qt2, qt3])
    t3 = threading.Thread(target=largest, args=[qt3, qt4])

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    t1.start()
    t2.start()
    t3.start()

    p1.daemon = True
    p2.daemon = True
    p3.daemon = True
    p1.start()
    p2.start()
    p3.start()

    start_p = time.time()
    # for word in dict2_list:
    #     q1.put(word)
    [q1.put(word) for word in dict2_list]

    largest_word = ""
    for word in range(len(dict2_list)):
        word = q4.get()
        if word[2]:
            largest_word = word[0]
    end_p = time.time()

    start_t = time.time()
    # for word in dict2_list:
    #     qt1.put(word)
    [qt1.put(tword) for tword in dict2_list]

    largest_tword = ""
    for word in range(len(dict2_list)):
        tword = qt4.get()
        if tword[2]:
            largest_tword = tword[0]
    end_t = time.time()

    print("(Processes) Largest: " + largest_word + " in "
          + str(end_p - start_p)[:4] + " sec")
    print("(Threads) Largest: " + largest_tword + " in "
          + str(end_t - start_t)[:4] + " sec")

    q1.join()
    q2.join()
    q3.join()

    qt1.join()
    qt2.join()
    qt3.join()
