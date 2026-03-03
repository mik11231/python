#!/usr/bin/env python3
"""Tests for Day 14: Docking Data using the provided examples."""

from day14 import parse_program, run_v1
from day14_part2 import run_v2

EXAMPLE_V1 = """\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""

EXAMPLE_V2 = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""


def test_part1_example():
    """Verify Part 1 example: sum of memory values after v1 mask is 165."""
    program = parse_program(EXAMPLE_V1)
    memory = run_v1(program)
    total = sum(memory.values())
    assert total == 165, f"Expected 165, got {total}"


def test_part2_example():
    """Verify Part 2 example: sum of memory values after v2 floating mask is 208."""
    program = parse_program(EXAMPLE_V2)
    memory = run_v2(program)
    total = sum(memory.values())
    assert total == 208, f"Expected 208, got {total}"


if __name__ == "__main__":
    test_part1_example()
    test_part2_example()
    print("All Day 14 tests passed.")
