"""Advent of Code 2018 solution module."""

from pathlib import Path


def load_polymer(path: Path) -> str:
    return path.read_text().strip()


def react(polymer: str) -> str:
    stack: list[str] = []
    for ch in polymer:
        if stack and stack[-1] != ch and stack[-1].lower() == ch.lower():
            stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)


def solve(polymer: str) -> int:
    best = len(polymer)
    for unit in "abcdefghijklmnopqrstuvwxyz":
        filtered = (ch for ch in polymer if ch.lower() != unit)
        reacted_len = len(react("".join(filtered)))
        if reacted_len < best:
            best = reacted_len
    return best


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d5_input.txt")
    print(solve(load_polymer(input_path)))
