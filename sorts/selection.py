def findSmallest(lst) {
  smallest = lst[0]
  ptr=1
  while ptr < len(lst) {
    if lst[ptr] < smallest {
      smallest = lst[ptr]
      Record position of smallest item
    }
    ptr++
  }
  return positionOfSmallest
}

void selectionSort() {
  Find position of smallest item
  Swap it with first position in list
  Repeat for 2nd smallest & 2nd pos, etc
  Stop when you're out of list
}
