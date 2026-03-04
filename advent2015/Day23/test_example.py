#!/usr/bin/env python3
"""Example smoke tests for Day 23."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day23 import solve as solve1, parse_program, run
from day23_part2 import solve as solve2


def main() -> None:
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    example = """inc a
jio a, +2
tpl a
inc a
"""
    prog = parse_program(example)
    # a=0: inc a -> 1, jio a, +2 -> a==1 so jump +2 -> tpl a (skip), inc a (skip)? No: jio jumps to next instruction +2, so we go to "inc a" (skip tpl). So pc: 0->1, 1: jio a,+2, a=1 so pc += 2 -> 3. inc a -> a=2. pc=4 exit. b=0.
    assert run(prog, 0, 0) == 0
    # a=1: inc a -> 2, jio a,+2 -> a!=1 so pc+=1 -> 2. tpl a -> 6, inc a -> 7. b=0.
    assert run(prog, 1, 0) == 0
    assert solve1(example) == 0
    assert solve2(example) == 0
    print("Day 23 examples OK")


if __name__ == "__main__":
    main()
