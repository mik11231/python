"""
advent2018/Day9/test_example.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2018.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

from day9 import play


def test_examples():
    """
    Run `test_examples` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert play(9, 25) == 32
    assert play(10, 1618) == 8317
    assert play(13, 7999) == 146373


if __name__ == "__main__":
    test_examples()
    print("ok")
