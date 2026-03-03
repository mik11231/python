#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 4: Giant Squid (Part 1)

Play bingo against a giant squid.  Given a sequence of drawn numbers and a set
of 5×5 bingo boards, find the *first* board to win.  The score is the sum of
all unmarked numbers on the winning board multiplied by the number that was
just called.

Algorithm
---------
For each board keep a set of unmarked numbers and track marked counts per row
and per column.  When any row or column reaches 5 marks the board wins.
O(d × b) where d = drawn numbers and b = number of boards.
"""

from pathlib import Path


def parse_bingo(text: str) -> tuple[list[int], list[list[list[int]]]]:
    """Parse bingo input into (drawn_numbers, boards).

    Each board is a 5×5 list of ints.
    """
    blocks = text.strip().split("\n\n")
    numbers = [int(x) for x in blocks[0].split(",")]
    boards: list[list[list[int]]] = []
    for block in blocks[1:]:
        board = [
            [int(x) for x in row.split()]
            for row in block.strip().splitlines()
        ]
        boards.append(board)
    return numbers, boards


def _make_board_state(board: list[list[int]]) -> dict:
    """Create tracking state for a single board."""
    unmarked: set[int] = set()
    position: dict[int, tuple[int, int]] = {}
    for r, row in enumerate(board):
        for c, val in enumerate(row):
            unmarked.add(val)
            position[val] = (r, c)
    return {
        "unmarked": unmarked,
        "position": position,
        "row_marks": [0] * 5,
        "col_marks": [0] * 5,
    }


def play_bingo(numbers: list[int], boards: list[list[list[int]]]) -> tuple[int, int]:
    """Play bingo and return (winning_board_index, score) for the first winner."""
    states = [_make_board_state(b) for b in boards]
    for num in numbers:
        for idx, state in enumerate(states):
            if num in state["position"]:
                r, c = state["position"][num]
                state["unmarked"].discard(num)
                state["row_marks"][r] += 1
                state["col_marks"][c] += 1
                if state["row_marks"][r] == 5 or state["col_marks"][c] == 5:
                    return idx, sum(state["unmarked"]) * num
    raise ValueError("No board wins")


def solve(input_path: str = "advent2021/Day4/d4_input.txt") -> int:
    """Read bingo input and return the score of the first winning board."""
    numbers, boards = parse_bingo(Path(input_path).read_text())
    _, score = play_bingo(numbers, boards)
    return score


if __name__ == "__main__":
    result = solve()
    print(f"First winning board score: {result}")
