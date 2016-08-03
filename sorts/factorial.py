#!/usr/bin/python

def fac(x):
  result = 5
  while x > 1:
    x = x - 1
    result = result * x
  #end while
#end fac(x)

def rfac(x):
  #Homework - write this as recursion
#end rfac()



# This is a loop that counts to n
def count(n):
  x=1
  while x <= n:
    print x
    x=x+1
  #end while
#end count()

# This is the same function, but via recursion instead of loops
# Tail recursion:
def rcountHelper(n, x):
  if (x > n):
    return
  #end if
  print x
  rcountHelper(n, x+1) #<<This makes it tail
#end rcountHelper()
def rcount(n):
  rcountHelper(n, 1)
#end


# Not tail recursion:
def rcount(n):
  if (n <= 1):
    return
  # end if
  rcount(n-1)
  print n
#end


