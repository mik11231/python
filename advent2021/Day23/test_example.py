#!/usr/bin/env python3
"""Tests for Day 23 using the example from the problem statement.

Example layout:
    #############
    #...........#
    ###B#C#B#D###
      #A#D#C#A#
      #########

Part 1 (room size 2): minimum energy = 12521.
Part 2 (room size 4, with inserted rows): minimum energy = 44169.
"""

from day23 import parse_input, solve_amphipod
from day23_part2 import expand_rooms

EXAMPLE = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""


def test_parse():
    """Verify rooms are parsed correctly from the example."""
    rooms = parse_input(EXAMPLE)
    assert rooms == [["B", "A"], ["C", "D"], ["B", "C"], ["D", "A"]]


def test_part1():
    """Verify Part 1: minimum energy = 12521."""
    rooms = parse_input(EXAMPLE)
    assert solve_amphipod(rooms, room_size=2) == 12521


def test_expand():
    """Verify room expansion for Part 2."""
    rooms = parse_input(EXAMPLE)
    expanded = expand_rooms(rooms)
    assert expanded == [
        ["B", "D", "D", "A"],
        ["C", "C", "B", "D"],
        ["B", "B", "A", "C"],
        ["D", "A", "C", "A"],
    ]


def test_part2():
    """Verify Part 2: minimum energy = 44169."""
    rooms = parse_input(EXAMPLE)
    expanded = expand_rooms(rooms)
    assert solve_amphipod(expanded, room_size=4) == 44169


if __name__ == "__main__":
    test_parse()
    print("PASS  Parse: rooms match expected layout")
    test_part1()
    print("PASS  Part 1: minimum energy = 12521")
    test_expand()
    print("PASS  Room expansion matches expected Part 2 layout")
    test_part2()
    print("PASS  Part 2: minimum energy = 44169")
    print("\nAll Day 23 tests passed!")
