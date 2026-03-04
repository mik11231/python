#!/usr/bin/python
"""
sorts/bubble.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: shared.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""


#Start at pos=0
#Compare lst[pos] to lst[pos+1]
#If out of order, swap
#pos++
#Repeat 'till out of list
#Now the largest item is "sorted" on the far right.
#Repeat until the whole thing's sorted.

