"""
advent2018/Day3/test_example.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2018.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

from day3 import solve as solve_part1
from day3_part2 import solve as solve_part2


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
    claims = [
        (1, 1, 3, 4, 4),
        (2, 3, 1, 4, 4),
        (3, 5, 5, 2, 2),
    ]
    assert solve_part1(claims) == 4


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
    claims = [
        (1, 1, 3, 4, 4),
        (2, 3, 1, 4, 4),
        (3, 5, 5, 2, 2),
    ]
    assert solve_part2(claims) == 3

if __name__ == "__main__":
    test_part1_example()
    test_part2_example()
    print("ok")
