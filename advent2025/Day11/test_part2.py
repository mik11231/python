#!/usr/bin/env python3
"""Day 11 Part 2 example test."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Day11.day11_part2 import count_paths_with_required_nodes, parse_graph


EXAMPLE = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""


def main() -> None:
    graph = parse_graph(EXAMPLE.splitlines())
    got = count_paths_with_required_nodes(graph, "svr", "out", ("dac", "fft"))
    expected = 2
    print(f"Day 11 Part 2 example paths: {got} (expected {expected})")
    if got != expected:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
