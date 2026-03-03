#!/usr/bin/env python3
"""Tests for Day 10: Syntax Scoring."""

from day10 import find_first_illegal, score_corrupted
from day10_part2 import completion_score

EXAMPLE_LINES = [
    "[({(<(())[]>[[{[]{<()<>>",
    "[(()[<>])]({[<{<<[]>>(",
    "{([(<{}[<>[]}>{[]{[(<()>",
    "(((({<>}<{<{<>}{[]{[]{}",
    "[[<[([]))<])]{}[}}]]>]]",
    "[{[{({}]{}}([{[{{{}}([]",
    "{<[[]]>}<{[{[{[]{()[[[]",
    "[<(<(<(<{}))><([]([]()",
    "<{([([[(<>()){}]>(<<{{",
    "<{([{{}}[<[[[<>{}]]]>[]]",
]


def test_corrupted_characters():
    """The five corrupted lines have first-illegal characters }, ), ], ), >."""
    expected = {
        2: "}",
        4: ")",
        5: "]",
        7: ")",
        8: ">",
    }
    for idx, char in expected.items():
        assert find_first_illegal(EXAMPLE_LINES[idx]) == char


def test_corruption_score():
    """Total syntax error score for the example is 26397."""
    assert score_corrupted(EXAMPLE_LINES) == 26397


def test_completion_scores():
    """Each incomplete line produces the documented autocomplete score."""
    expected = {
        0: 288957,
        1: 5566,
        3: 1480781,
        6: 995444,
        9: 294,
    }
    for idx, score in expected.items():
        assert completion_score(EXAMPLE_LINES[idx]) == score


def test_middle_score():
    """The middle autocomplete score for the example is 288957."""
    scores = sorted(
        s for line in EXAMPLE_LINES
        if (s := completion_score(line)) is not None
    )
    assert scores[len(scores) // 2] == 288957
