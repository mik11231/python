#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 4: Giant Squid (Part 2)

Instead of finding the first bingo board to win, find the *last* board to win
and return its score.

Algorithm
---------
Same marking logic as Part 1, but track which boards have already won and
continue until every board has won.  The answer is the score of the final
winner.
"""

from pathlib import Path

from day4 import parse_bingo, _make_board_state


def play_bingo_last(numbers: list[int], boards: list[list[list[int]]]) -> tuple[int, int]:
    """Play bingo to completion and return (last_board_index, score)."""
    states = [_make_board_state(b) for b in boards]
    won: set[int] = set()
    total = len(boards)
    for num in numbers:
        for idx, state in enumerate(states):
            if idx in won:
                continue
            if num in state["position"]:
                r, c = state["position"][num]
                state["unmarked"].discard(num)
                state["row_marks"][r] += 1
                state["col_marks"][c] += 1
                if state["row_marks"][r] == 5 or state["col_marks"][c] == 5:
                    won.add(idx)
                    if len(won) == total:
                        return idx, sum(state["unmarked"]) * num
    raise ValueError("Not all boards win")


def solve(input_path: str = "advent2021/Day4/d4_input.txt") -> int:
    """Read bingo input and return the score of the last winning board."""
    numbers, boards = parse_bingo(Path(input_path).read_text())
    _, score = play_bingo_last(numbers, boards)
    return score


if __name__ == "__main__":
    result = solve()
    print(f"Last winning board score: {result}")
