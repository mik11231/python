#!/usr/bin/env python3
"""Tests for Day 20 using the example from the problem statement.

The example algorithm is 512 characters (starting with '..#.#..#####...').
The example image is a 5x5 grid with 10 lit pixels.

Part 1: After 2 enhancements, 35 pixels are lit.
Part 2: After 50 enhancements, 3351 pixels are lit.
"""

from day20 import enhance, parse_input

EXAMPLE_ALGORITHM = (
    "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##"
    "#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###"
    ".######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#."
    ".#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#....."
    ".#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.."
    "...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#....."
    "..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
)

EXAMPLE_IMAGE = """\
#..#.
#....
##..#
..#..
..###"""

EXAMPLE_INPUT = EXAMPLE_ALGORITHM + "\n\n" + EXAMPLE_IMAGE


def test_parse():
    """Verify parsing produces the correct algorithm length and pixel count."""
    algo, image = parse_input(EXAMPLE_INPUT)
    assert len(algo) == 512
    assert len(image) == 10


def test_part1():
    """Verify Part 1: 35 lit pixels after 2 enhancements."""
    algo, image = parse_input(EXAMPLE_INPUT)
    default = "."
    for _ in range(2):
        image, default = enhance(image, algo, default)
    assert len(image) == 35


def test_part2():
    """Verify Part 2: 3351 lit pixels after 50 enhancements."""
    algo, image = parse_input(EXAMPLE_INPUT)
    default = "."
    for _ in range(50):
        image, default = enhance(image, algo, default)
    assert len(image) == 3351


if __name__ == "__main__":
    test_parse()
    print("PASS  Parse: algorithm length 512, 10 lit pixels")
    test_part1()
    print("PASS  Part 1: 35 lit pixels after 2 enhancements")
    test_part2()
    print("PASS  Part 2: 3351 lit pixels after 50 enhancements")
    print("\nAll Day 20 tests passed!")
