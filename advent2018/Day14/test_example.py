"""
advent2018/Day14/test_example.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2018.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

from day14 import solve as solve_part1
from day14_part2 import solve as solve_part2


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
    assert solve_part1(9) == '5158916779'
    assert solve_part1(5) == '0124515891'
    assert solve_part1(18) == '9251071085'
    assert solve_part1(2018) == '5941429882'


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
    assert solve_part2('51589') == 9
    assert solve_part2('01245') == 5
    assert solve_part2('92510') == 18
    assert solve_part2('59414') == 2018


if __name__ == '__main__':
    test_part1_examples()
    test_part2_examples()
    print('ok')
