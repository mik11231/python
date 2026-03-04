"""
advent2018/Day6/test_example.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2018.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

from day6 import solve as solve_part1
from day6_part2 import solve as solve_part2


EXAMPLE_POINTS = [
    (1, 1),
    (1, 6),
    (8, 3),
    (3, 4),
    (5, 5),
    (8, 9),
]


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
    assert solve_part1(EXAMPLE_POINTS) == 17


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
    assert solve_part2(EXAMPLE_POINTS, distance_limit=32) == 16


if __name__ == "__main__":
    test_part1_example()
    test_part2_example()
    print("ok")
