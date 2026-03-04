"""
advent2018/Day12/test_example.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2018.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

from day12 import load, solve
from day12_part2 import solve as solve_p2


def test_example_part1(tmp_path):
    """
    Run `test_example_part1` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: tmp_path.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    sample = '''
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
'''.strip()
    p = tmp_path / 'in.txt'
    p.write_text(sample)
    s, r = load(p)
    assert solve(s, r) == 325


def test_part2_smoke(tmp_path):
    """
    Run `test_part2_smoke` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: tmp_path.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    sample = '''
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
'''.strip()
    p = tmp_path / 'in.txt'
    p.write_text(sample)
    s, r = load(p)
    assert solve_p2(s, r, target=200) > 0


if __name__ == '__main__':
    from pathlib import Path
    t = Path('/tmp/day12_test')
    t.mkdir(exist_ok=True)
    class T:
        def __truediv__(self, o):
            """
            Run `__truediv__` as a clearly documented algorithm stage.
            
            Methodology:
            - Treat this function as one deterministic step in the Advent pipeline.
            - Keep parsing, state transitions, and result emission easy to audit.
            - Favor explicit control flow so behavior can be reasoned about from docs alone.
            
            Parameters: self, o.
            - Produces side effects required by the caller (output/mutation/control flow).
            """
            return t / o
    test_example_part1(T())
    test_part2_smoke(T())
    print('ok')
