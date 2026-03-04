"""
advent2018/Day11/test_example.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2018.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

from day11 import power_level, solve as solve_part1
from day11_part2 import solve as solve_part2


def test_power_level_examples():
    """
    Run `test_power_level_examples` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert power_level(3, 5, 8) == 4
    assert power_level(122, 79, 57) == -5
    assert power_level(217, 196, 39) == 0
    assert power_level(101, 153, 71) == 4


def test_part1_examples():
    """
    Run `test_part1_examples` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_part1(18) == "33,45"
    assert solve_part1(42) == "21,61"


def test_part2_examples():
    """
    Run `test_part2_examples` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_part2(18) == "90,269,16"
    assert solve_part2(42) == "232,251,12"


if __name__ == "__main__":
    test_power_level_examples()
    test_part1_examples()
    test_part2_examples()
    print("ok")
