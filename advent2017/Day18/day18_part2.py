#!/usr/bin/env python3
"""Advent of Code 2017 Day 18 Part 2."""

from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Prog:
    ip: int
    r: defaultdict[str, int]
    q: deque[int]
    sent: int = 0
    blocked: bool = False
    done: bool = False


def solve(s: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    p = [ln.split() for ln in s.splitlines() if ln.strip()]

    def val(pr: Prog, x: str) -> int:
        """
        Run `val` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: pr, x.
        - Returns the computed result for this stage of the pipeline.
        """
        return int(x) if x.lstrip("-").isdigit() else pr.r[x]

    a = Prog(0, defaultdict(int), deque())
    b = Prog(0, defaultdict(int), deque())
    a.r["p"] = 0
    b.r["p"] = 1

    def step(cur: Prog, oth: Prog) -> None:
        """
        Run `step` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: cur, oth.
        - Returns the computed result for this stage of the pipeline.
        """
        if not (0 <= cur.ip < len(p)):
            cur.done = True
            cur.blocked = True
            return
        op, *x = p[cur.ip]
        if op == "snd":
            oth.q.append(val(cur, x[0]))
            cur.sent += 1
            cur.ip += 1
            cur.blocked = False
        elif op == "set":
            cur.r[x[0]] = val(cur, x[1])
            cur.ip += 1
            cur.blocked = False
        elif op == "add":
            cur.r[x[0]] += val(cur, x[1])
            cur.ip += 1
            cur.blocked = False
        elif op == "mul":
            cur.r[x[0]] *= val(cur, x[1])
            cur.ip += 1
            cur.blocked = False
        elif op == "mod":
            cur.r[x[0]] %= val(cur, x[1])
            cur.ip += 1
            cur.blocked = False
        elif op == "rcv":
            if cur.q:
                cur.r[x[0]] = cur.q.popleft()
                cur.ip += 1
                cur.blocked = False
            else:
                cur.blocked = True
        elif op == "jgz":
            if val(cur, x[0]) > 0:
                cur.ip += val(cur, x[1])
            else:
                cur.ip += 1
            cur.blocked = False

    while True:
        step(a, b)
        step(b, a)
        if (a.blocked or a.done) and (b.blocked or b.done):
            return b.sent


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d18_input.txt").read_text(encoding="utf-8")))
