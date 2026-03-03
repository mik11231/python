#!/usr/bin/env python3
"""Tests for Day 8 using the example from the problem statement.

Example program:
    nop +0 / acc +1 / jmp +4 / acc +3 / jmp -3 / acc -99 / acc +1 / jmp -4 / acc +6

Part 1: Infinite loop detected — accumulator = 5.
Part 2: Swap ``jmp -4`` (index 7) to ``nop -4`` — program terminates with
        accumulator = 8.
"""

from day8 import parse_program, run_program
from day8_part2 import find_fix

EXAMPLE = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""


def test_part1():
    """Verify Part 1 example: accumulator is 5 before infinite loop."""
    program = parse_program(EXAMPLE)
    acc, terminated = run_program(program)
    assert not terminated, "Expected an infinite loop"
    assert acc == 5, f"Expected accumulator 5, got {acc}"
    print(f"PASS  Part 1: accumulator = {acc}")


def test_part2():
    """Verify Part 2 example: swapping jmp to nop yields accumulator 8."""
    program = parse_program(EXAMPLE)
    acc = find_fix(program)
    assert acc == 8, f"Expected accumulator 8, got {acc}"
    print(f"PASS  Part 2: accumulator = {acc}")


if __name__ == "__main__":
    test_part1()
    test_part2()
    print("\nAll Day 8 tests passed!")
