#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 20: Trench Map (Part 1)

An image enhancement algorithm (512-char string) maps each pixel's 3x3
neighbourhood to a new pixel value.  The image is infinite; pixels outside
the known region share a single "default" value that starts as dark ('.').

If algorithm[0] == '#' and algorithm[511] == '.', the infinite void toggles
between lit and dark on every step.

Algorithm
---------
Represent the image as a set of lit-pixel coordinates.  On each enhancement
step, expand the bounding box by 1 in every direction, compute the 9-bit
index for each cell from its 3x3 neighbourhood, and look up the result in
the algorithm string.  Track the default pixel for the infinite background
separately.
"""

from pathlib import Path


def parse_input(text: str) -> tuple[str, set[tuple[int, int]]]:
    """Return (algorithm, lit_pixels) from the raw puzzle text.

    The algorithm is a single 512-character string.  The image is returned
    as a set of (row, col) coordinates of '#' pixels.
    """
    parts = text.strip().split("\n\n")
    algorithm = parts[0].replace("\n", "")
    image_lines = parts[1].splitlines()
    lit: set[tuple[int, int]] = set()
    for r, line in enumerate(image_lines):
        for c, ch in enumerate(line):
            if ch == "#":
                lit.add((r, c))
    return algorithm, lit


def enhance(
    image: set[tuple[int, int]],
    algorithm: str,
    default_pixel: str,
) -> tuple[set[tuple[int, int]], str]:
    """Apply one enhancement step.

    Returns (new_image, new_default_pixel).  *default_pixel* is the value
    of every pixel outside the tracked bounding box ('.' or '#').
    """
    if not image:
        idx = 0 if default_pixel == "." else 511
        return set(), algorithm[idx]

    min_r = min(r for r, _ in image)
    max_r = max(r for r, _ in image)
    min_c = min(c for _, c in image)
    max_c = max(c for _, c in image)

    default_is_lit = default_pixel == "#"
    new_image: set[tuple[int, int]] = set()

    for r in range(min_r - 1, max_r + 2):
        for c in range(min_c - 1, max_c + 2):
            bits = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    bits <<= 1
                    nr, nc = r + dr, c + dc
                    if min_r <= nr <= max_r and min_c <= nc <= max_c:
                        if (nr, nc) in image:
                            bits |= 1
                    elif default_is_lit:
                        bits |= 1
            if algorithm[bits] == "#":
                new_image.add((r, c))

    void_index = 0 if default_pixel == "." else 511
    return new_image, algorithm[void_index]


def solve(input_path: str = "advent2021/Day20/d20_input.txt") -> int:
    """Enhance the image twice and return the number of lit pixels."""
    text = Path(input_path).read_text()
    algorithm, image = parse_input(text)
    default = "."
    for _ in range(2):
        image, default = enhance(image, algorithm, default)
    return len(image)


if __name__ == "__main__":
    print(f"Lit pixels after 2 enhancements: {solve()}")
