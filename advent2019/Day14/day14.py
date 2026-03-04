"""Advent of Code 2019 Day 14 Part 1."""

from collections import defaultdict
from math import ceil
from pathlib import Path


def parse(s: str):
    """
    Run `parse` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    rec = {}
    for line in s.splitlines():
        if not line.strip():
            continue
        lhs, rhs = line.split(' => ')
        out_n, out_c = rhs.split()
        ins = []
        for part in lhs.split(', '):
            n, c = part.split()
            ins.append((int(n), c))
        rec[out_c] = (int(out_n), ins)
    return rec


def ore_for_fuel(rec, fuel=1):
    """
    Run `ore_for_fuel` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: rec, fuel.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    need = defaultdict(int, {'FUEL': fuel})
    extra = defaultdict(int)

    while True:
        chem = next((c for c, n in need.items() if c != 'ORE' and n > 0), None)
        if chem is None:
            break
        qty = need[chem]
        need[chem] = 0

        use = min(qty, extra[chem])
        qty -= use
        extra[chem] -= use
        if qty == 0:
            continue

        out_qty, ins = rec[chem]
        batches = ceil(qty / out_qty)
        extra[chem] += batches * out_qty - qty
        for n, c in ins:
            need[c] += n * batches

    return need['ORE']


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
    return ore_for_fuel(parse(s), 1)


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d14_input.txt').read_text()))
