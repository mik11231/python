#!/usr/bin/env python3
"""Day 11 example test."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Day11.day11 import count_paths_you_to_out, parse_graph


EXAMPLE = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""


def main() -> None:
    graph = parse_graph(EXAMPLE.splitlines())
    got = count_paths_you_to_out(graph)
    expected = 5
    print(f"Day 11 example paths: {got} (expected {expected})")
    if got != expected:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
