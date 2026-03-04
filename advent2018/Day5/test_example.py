"""
advent2018/Day5/test_example.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2018.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

from day5 import react, solve as solve_part1
from day5_part2 import solve as solve_part2


EXAMPLE = "dabAcCaCBAcCcaDA"


def test_reaction_example():
    """
    Run `test_reaction_example` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert react(EXAMPLE) == "dabCBAcaDA"


def test_part1_example():
    """
    Run `test_part1_example` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_part1(EXAMPLE) == 10


def test_part2_example():
    """
    Run `test_part2_example` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_part2(EXAMPLE) == 4


if __name__ == "__main__":
    test_reaction_example()
    test_part1_example()
    test_part2_example()
    print("ok")
