"""Advent of Code 2018 solution module."""

from pathlib import Path


def first_appearance(target: str) -> int:
    """Return first index where target digit-string appears in the scoreboard."""
    want = [int(c) for c in target]
    m = len(want)

    board = [3, 7]
    a, b = 0, 1

    while True:
        s = board[a] + board[b]
        new_digits = [1, s % 10] if s >= 10 else [s]

        for d in new_digits:
            board.append(d)
            if len(board) >= m and board[-m:] == want:
                return len(board) - m

        a = (a + 1 + board[a]) % len(board)
        b = (b + 1 + board[b]) % len(board)


def solve(target: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: target.
    - Returns the computed result for this stage of the pipeline.
    """
    return first_appearance(target)


if __name__ == '__main__':
    s = Path(__file__).with_name('d14_input.txt').read_text().strip()
    print(solve(s))
