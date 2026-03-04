"""Advent of Code 2018 solution module."""

import re
from collections import Counter
from pathlib import Path

CLAIM_RE = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")


def load_claims(path: Path) -> list[tuple[int, int, int, int, int]]:
    """
    Run `load_claims` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    claims = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        claim_id, x, y, width, height = map(int, CLAIM_RE.fullmatch(line).groups())
        claims.append((claim_id, x, y, width, height))
    return claims


def build_fabric_counts(claims: list[tuple[int, int, int, int, int]]) -> Counter[tuple[int, int]]:
    """
    Run `build_fabric_counts` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: claims.
    - Returns the computed result for this stage of the pipeline.
    """
    fabric = Counter()
    for _, x, y, width, height in claims:
        for xi in range(x, x + width):
            for yi in range(y, y + height):
                fabric[(xi, yi)] += 1
    return fabric


def solve(claims: list[tuple[int, int, int, int, int]]) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: claims.
    - Returns the computed result for this stage of the pipeline.
    """
    fabric = build_fabric_counts(claims)
    for claim_id, x, y, width, height in claims:
        if all(fabric[(xi, yi)] == 1 for xi in range(x, x + width) for yi in range(y, y + height)):
            return claim_id
    raise RuntimeError("No non-overlapping claim found")


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d3_input.txt")
    print(solve(load_claims(input_path)))
