"""Advent of Code 2018 solution module."""

from pathlib import Path


def load_polymer(path: Path) -> str:
    """
    Run `load_polymer` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    return path.read_text().strip()


def react(polymer: str) -> str:
    """
    Run `react` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: polymer.
    - Returns the computed result for this stage of the pipeline.
    """
    stack: list[str] = []
    for ch in polymer:
        if stack and stack[-1] != ch and stack[-1].lower() == ch.lower():
            stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)


def solve(polymer: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: polymer.
    - Returns the computed result for this stage of the pipeline.
    """
    return len(react(polymer))


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d5_input.txt")
    print(solve(load_polymer(input_path)))
