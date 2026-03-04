"""Advent of Code 2018 solution module."""

from functools import lru_cache
from pathlib import Path


def load(path: Path):
    """
    Run `load` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    depth = int(lines[0].split(': ')[1])
    tx, ty = map(int, lines[1].split(': ')[1].split(','))
    return depth, tx, ty


def make_erosion(depth: int, tx: int, ty: int):
    """Return memoized erosion-level function for this cave definition."""

    @lru_cache(None)
    def erosion(x: int, y: int) -> int:
        """
        Run `erosion` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: x, y.
        - Returns the computed result for this stage of the pipeline.
        """
        if (x, y) in ((0, 0), (tx, ty)):
            gi = 0
        elif y == 0:
            gi = x * 16807
        elif x == 0:
            gi = y * 48271
        else:
            gi = erosion(x - 1, y) * erosion(x, y - 1)
        return (gi + depth) % 20183

    return erosion


def solve(depth: int, tx: int, ty: int) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: depth, tx, ty.
    - Returns the computed result for this stage of the pipeline.
    """
    erosion = make_erosion(depth, tx, ty)
    return sum(erosion(x, y) % 3 for y in range(ty + 1) for x in range(tx + 1))


if __name__ == '__main__':
    d, tx, ty = load(Path(__file__).with_name('d22_input.txt'))
    print(solve(d, tx, ty))
