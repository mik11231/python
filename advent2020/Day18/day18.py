#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 18: Operation Order (Part 1)

Evaluate math expressions where ``+`` and ``*`` have **equal** precedence
(left-to-right), with parentheses overriding order.

Algorithm
---------
A small recursive-descent parser (or an operator-precedence parser) that
respects a configurable precedence table.

``evaluate(expr, precedence)`` accepts a dict mapping operator characters to
integer precedence levels.  Higher numbers bind tighter.  For Part 1 both
``+`` and ``*`` get the same level; for Part 2 ``+`` is higher.

Internally the parser uses two stacks (values and operators) and flushes
operators of sufficient precedence before pushing a new one, the classic
shunting-yard approach.
"""

from pathlib import Path

EQUAL_PRECEDENCE: dict[str, int] = {"+": 1, "*": 1}


def _apply(op: str, a: int, b: int) -> int:
    """Apply a binary operator ('+' or '*') to two operands."""
    if op == "+":
        return a + b
    return a * b


def _flush(ops: list[str], vals: list[int], min_prec: int, prec: dict[str, int]) -> None:
    """Pop and apply operators whose precedence is >= *min_prec*."""
    while ops and ops[-1] != "(" and prec.get(ops[-1], 0) >= min_prec:
        b, a = vals.pop(), vals.pop()
        vals.append(_apply(ops.pop(), a, b))


def evaluate(expr: str, precedence: dict[str, int] | None = None) -> int:
    """Evaluate a single expression string under the given precedence rules.

    *precedence* maps ``"+"`` and ``"*"`` to integer levels.
    Defaults to :data:`EQUAL_PRECEDENCE` (Part 1 rules).
    """
    if precedence is None:
        precedence = EQUAL_PRECEDENCE
    ops: list[str] = []
    vals: list[int] = []
    tokens = expr.replace("(", "( ").replace(")", " )").split()

    for tok in tokens:
        if tok.isdigit():
            vals.append(int(tok))
        elif tok == "(":
            ops.append(tok)
        elif tok == ")":
            _flush(ops, vals, 0, precedence)
            ops.pop()  # remove the "("
        else:
            _flush(ops, vals, precedence[tok], precedence)
            ops.append(tok)

    _flush(ops, vals, 0, precedence)
    return vals[0]


def solve(input_path: str = "advent2020/Day18/d18_input.txt") -> int:
    """Sum the results of every expression using equal-precedence rules."""
    lines = Path(input_path).read_text().strip().splitlines()
    return sum(evaluate(line) for line in lines)


if __name__ == "__main__":
    result = solve()
    print(f"Sum of all expressions (equal precedence): {result}")
