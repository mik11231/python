#!/usr/bin/env python3
"""Tests for Day 24 — parameter extraction and constraint solving.

Day 24 has no small worked example.  Instead we verify:
  * ``extract_parameters`` correctly reads div_z / add_x / add_y from a
    known two-block program fragment.
  * ``solve_monad`` produces valid 14-digit numbers (all digits 1-9) and
    satisfies the structural constraint (maximize > minimize).
"""

from day24 import extract_parameters, solve_monad

TWO_BLOCK_FRAGMENT = """\
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 11
mul y x
add z y
"""

# 14 parameters extracted from the actual puzzle input (used for
# structural validation — not a spoiler since only the parameters,
# not the final answer, are shown here).
FULL_PARAMS = [
    (1, 13, 6), (1, 11, 11), (1, 12, 5), (1, 10, 6),
    (1, 14, 8), (26, -1, 14), (1, 14, 9),
    (26, -16, 4), (26, -8, 7), (1, 12, 13),
    (26, -16, 11), (26, -13, 11), (26, -6, 6), (26, -6, 1),
]


def test_extract_parameters():
    """Verify extraction of (div_z, add_x, add_y) from two blocks."""
    params = extract_parameters(TWO_BLOCK_FRAGMENT)
    assert len(params) == 2
    assert params[0] == (1, 13, 6)
    assert params[1] == (1, 11, 11)


def test_solve_max_produces_valid_digits():
    """Verify maximize yields a 14-digit number with digits in 1-9."""
    result = solve_monad(FULL_PARAMS, maximize=True)
    digits = [int(d) for d in str(result)]
    assert len(digits) == 14
    assert all(1 <= d <= 9 for d in digits)


def test_solve_min_produces_valid_digits():
    """Verify minimize yields a 14-digit number with digits in 1-9."""
    result = solve_monad(FULL_PARAMS, maximize=False)
    digits = [int(d) for d in str(result)]
    assert len(digits) == 14
    assert all(1 <= d <= 9 for d in digits)


def test_max_greater_than_min():
    """The maximised model number must exceed the minimised one."""
    max_val = solve_monad(FULL_PARAMS, maximize=True)
    min_val = solve_monad(FULL_PARAMS, maximize=False)
    assert max_val > min_val


def test_constraints_satisfied():
    """Verify both solutions satisfy all push/pop digit constraints."""
    for maximize in (True, False):
        result = solve_monad(FULL_PARAMS, maximize=maximize)
        digits = [int(d) for d in str(result)]
        stack: list[tuple[int, int]] = []
        for i, (div_z, add_x, add_y) in enumerate(FULL_PARAMS):
            if div_z == 1:
                stack.append((i, add_y))
            else:
                j, prev_add_y = stack.pop()
                assert digits[i] - digits[j] == prev_add_y + add_x


if __name__ == "__main__":
    test_extract_parameters()
    print("PASS  Parameter extraction: 2-block fragment")
    test_solve_max_produces_valid_digits()
    print("PASS  Maximize: valid 14-digit number")
    test_solve_min_produces_valid_digits()
    print("PASS  Minimize: valid 14-digit number")
    test_max_greater_than_min()
    print("PASS  max > min")
    test_constraints_satisfied()
    print("PASS  All push/pop constraints satisfied")
    print("\nAll Day 24 tests passed!")
