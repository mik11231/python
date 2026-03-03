#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 24: Arithmetic Logic Unit (Part 1)

The MONAD program validates 14-digit model numbers.  It consists of 14
nearly-identical blocks, each consuming one input digit.

Analysis
--------
Each block operates on register *z* as a base-26 stack:

* When ``div z 1``  (push):  z = z * 26 + (digit + add_y)
* When ``div z 26`` (pop):   the top-of-stack value plus *add_x* must
  equal the current digit for z to shrink; otherwise z grows further.

For z to reach 0 at the end, every push must be matched by a pop.
This yields 7 linear constraints of the form::

    digit[pop_pos] - digit[push_pos] == add_y[push_pos] + add_x[pop_pos]

We solve these constraints greedily: for Part 1 we maximise each digit
pair (prefer 9 where possible); for Part 2 we minimise (prefer 1).

Exports: ``extract_parameters``, ``solve_monad``.
"""

from pathlib import Path


def extract_parameters(
    program_text: str,
) -> list[tuple[int, int, int]]:
    """Extract (div_z, add_x, add_y) for each of the 14 blocks.

    Each block is exactly 18 instructions.  The three key parameters sit
    at fixed offsets within each block:
        line  4: ``div z <div_z>``
        line  5: ``add x <add_x>``
        line 15: ``add y <add_y>``
    """
    lines = program_text.strip().splitlines()
    params: list[tuple[int, int, int]] = []
    for i in range(0, len(lines), 18):
        block = lines[i : i + 18]
        div_z = int(block[4].split()[-1])
        add_x = int(block[5].split()[-1])
        add_y = int(block[15].split()[-1])
        params.append((div_z, add_x, add_y))
    return params


def solve_monad(
    params: list[tuple[int, int, int]],
    maximize: bool = True,
) -> int:
    """Return the largest (maximize=True) or smallest valid model number.

    Walks the 14 parameter blocks, pairing each pop with its matching
    push via a stack, then choosing the optimal digit for each pair.
    """
    digits = [0] * 14
    stack: list[tuple[int, int]] = []  # (block_index, add_y)

    for i, (div_z, add_x, add_y) in enumerate(params):
        if div_z == 1:
            stack.append((i, add_y))
        else:
            j, prev_add_y = stack.pop()
            delta = prev_add_y + add_x  # digit[i] - digit[j]
            if maximize:
                if delta >= 0:
                    digits[i] = 9
                    digits[j] = 9 - delta
                else:
                    digits[j] = 9
                    digits[i] = 9 + delta
            else:
                if delta >= 0:
                    digits[j] = 1
                    digits[i] = 1 + delta
                else:
                    digits[i] = 1
                    digits[j] = 1 - delta

    return int("".join(str(d) for d in digits))


def solve(input_path: str = "advent2021/Day24/d24_input.txt") -> int:
    """Return the largest accepted 14-digit model number."""
    text = Path(input_path).read_text()
    params = extract_parameters(text)
    return solve_monad(params, maximize=True)


if __name__ == "__main__":
    print(f"Largest valid model number: {solve()}")
