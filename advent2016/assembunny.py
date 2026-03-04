#!/usr/bin/env python3
"""Assembunny interpreter utilities for Advent of Code 2016."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RunResult:
    """Execution result with registers and optional output stream."""

    regs: dict[str, int]
    output: list[int]


def parse_program(s: str) -> list[list[str]]:
    """Parse whitespace-separated assembunny instructions."""
    return [ln.split() for ln in s.splitlines() if ln.strip()]


def run_program(
    program: list[list[str]],
    regs: dict[str, int] | None = None,
    max_steps: int | None = None,
    max_output: int | None = None,
) -> RunResult:
    """Run assembunny program with optional toggle/out and light peephole opts."""
    p = [ins[:] for ins in program]
    r = {"a": 0, "b": 0, "c": 0, "d": 0}
    if regs:
        r.update(regs)

    def val(x: str) -> int:
        """
        Run `val` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: x.
        - Returns the computed result for this stage of the pipeline.
        """
        if x.lstrip("-").isdigit():
            return int(x)
        return r.get(x, 0)

    out: list[int] = []
    pc = 0
    steps = 0

    while 0 <= pc < len(p):
        if max_steps is not None and steps >= max_steps:
            break
        steps += 1

        # Multiply loop optimization:
        # cpy X Y; inc A; dec Y; jnz Y -2; dec B; jnz B -5
        if pc + 5 < len(p):
            i0, i1, i2, i3, i4, i5 = p[pc : pc + 6]
            if (
                i0[0] == "cpy"
                and i1[0] == "inc"
                and i2[0] == "dec"
                and i3 == ["jnz", i2[1], "-2"]
                and i4[0] == "dec"
                and i5 == ["jnz", i4[1], "-5"]
                and len(i0) == 3
            ):
                x, y = i0[1], i0[2]
                a = i1[1]
                b = i4[1]
                if y in r and a in r and b in r:
                    r[a] += val(x) * r[b]
                    r[y] = 0
                    r[b] = 0
                    pc += 6
                    continue

        # Add loop optimization: inc A; dec B; jnz B -2
        if pc + 2 < len(p):
            i0, i1, i2 = p[pc : pc + 3]
            if i0[0] == "inc" and i1[0] == "dec" and i2 == ["jnz", i1[1], "-2"]:
                a, b = i0[1], i1[1]
                if a in r and b in r:
                    r[a] += r[b]
                    r[b] = 0
                    pc += 3
                    continue

        ins = p[pc]
        op = ins[0]

        if op == "cpy":
            x, y = ins[1], ins[2]
            if y in r:
                r[y] = val(x)
            pc += 1
        elif op == "inc":
            x = ins[1]
            if x in r:
                r[x] += 1
            pc += 1
        elif op == "dec":
            x = ins[1]
            if x in r:
                r[x] -= 1
            pc += 1
        elif op == "jnz":
            x, y = ins[1], ins[2]
            if val(x) != 0:
                pc += val(y)
            else:
                pc += 1
        elif op == "tgl":
            x = ins[1]
            t = pc + val(x)
            if 0 <= t < len(p):
                tgt = p[t]
                if len(tgt) == 2:
                    tgt[0] = "dec" if tgt[0] == "inc" else "inc"
                elif len(tgt) == 3:
                    tgt[0] = "cpy" if tgt[0] == "jnz" else "jnz"
            pc += 1
        elif op == "out":
            out.append(val(ins[1]))
            pc += 1
            if max_output is not None and len(out) >= max_output:
                break
        else:
            pc += 1

    return RunResult(r, out)
