#!/usr/bin/env python3
"""Tests for Day 25 using the example from the problem statement.

Example grid (10x10):
    v...>>.vv>
    .vv>>.vv..
    >>.>v>...v
    >>v>>.>.v.
    v>v.vv.v..
    >.>>..v...
    .vv..>.>v.
    v.v..>>v.v
    ....v..v.>

Part 1: sea cucumbers stop moving at step 58.
Part 2: Day 25 has no Part 2.
"""

from day25 import parse_grid, simulate
from day25_part2 import solve as solve_part2

EXAMPLE = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""


def test_parse():
    """Verify grid dimensions and cucumber counts."""
    rows, cols, east, south = parse_grid(EXAMPLE)
    assert rows == 9
    assert cols == 10
    assert len(east) + len(south) > 0


def test_part1():
    """Verify Part 1: movement stops at step 58."""
    rows, cols, east, south = parse_grid(EXAMPLE)
    assert simulate(rows, cols, east, south) == 58


def test_part2():
    """Day 25 Part 2 is a freebie — confirm the placeholder works."""
    msg = solve_part2()
    assert "free" in msg.lower() or "Christmas" in msg


if __name__ == "__main__":
    test_parse()
    print("PASS  Parse: grid 9x10 with cucumbers")
    test_part1()
    print("PASS  Part 1: stops at step 58")
    test_part2()
    print("PASS  Part 2: placeholder message")
    print("\nAll Day 25 tests passed!")
