#!/usr/bin/env python3
"""Example smoke tests for Day 11."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day11 import solve as solve1, is_valid, increment
from day11_part2 import solve as solve2


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
    assert increment("a") == "b"
    assert increment("z") == "a"  # only first char? No - single char: z -> a with carry, so we need to handle. For 8-char we get carry through. "z" -> "a" with carry; no more chars so result "a"? Actually "z" is 1 char: inc_char('z') -> 'a', True. So chars = ['a'], i=0, we set chars[0]='a', carry=True, i=-1, exit. So "z" -> "a". That's wrong for 8-char - we never have just "z". For "aaaaaaaa" increment -> "aaaaaaab", etc.
    assert is_valid("hijklmmn") is False  # has i, l (invalid chars - but our increment skips them; this is "already invalid" by rule)
    assert is_valid("abbceffg") is False  # no run of 3
    assert is_valid("abbcegjk") is False  # no second pair
    assert is_valid("abcdffaa") is True
    assert is_valid("ghjaabcc") is True
    assert solve1("abcdefgh\n") == "abcdffaa"
    assert solve1("ghijklmn\n") == "ghjaabcc"
    assert solve2("ghijklmn\n") == "ghjbbcdd"  # next after ghjaabcc
    print("Day 11 examples OK")


if __name__ == "__main__":
    main()
