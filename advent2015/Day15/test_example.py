#!/usr/bin/env python3
"""Example smoke tests for Day 15."""

from day15 import solve as solve1
from day15_part2 import solve as solve2


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
    example = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""
    # 44 butterscotch, 56 cinnamon: cap=44*(-1)+56*2=68, dur=44*(-2)+56*3=80, flv=44*6+56*(-2)=152, tex=44*3+56*(-1)=76 -> 68*80*152*76 = 62842880
    assert solve1(example) == 62842880, solve1(example)
    # Part 2: exactly 500 cal. 40 butterscotch (320), 60 cinnamon (180) = 500. cap=80, dur=0 -> 0. Need to find valid mix: 50*8+50*3=550 no. 44*8+56*3=352+168=520. 40*8+60*3=320+180=500. 40*-1+60*2=80, 40*-2+60*3=100, 40*6+60*(-2)=120, 40*3+60*(-1)=60 -> 80*100*120*60 = 57600000
    assert solve2(example) == 57600000, solve2(example)
    print("Part 1 and Part 2 examples: OK")


if __name__ == "__main__":
    main()
