#!/usr/bin/env python3
"""Tests for Day 22 using examples from the problem statement.

Small example (4 steps):  39 ON cubes.
Larger example (22 steps, init region -50..50):  590784 ON cubes.
The inclusion-exclusion method (Part 2) is cross-validated against the
brute-force result for the clipped 22-step example.
"""

from day22 import parse_steps
from day22_part2 import count_on_cubes

SMALL_EXAMPLE = """\
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
"""

LARGE_EXAMPLE = """\
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
"""


def _clip_steps(steps, lo=-50, hi=50):
    """Clip step ranges to [lo, hi] and discard steps that vanish."""
    clipped = []
    for action, x1, x2, y1, y2, z1, z2 in steps:
        cx1, cx2 = max(x1, lo), min(x2, hi)
        cy1, cy2 = max(y1, lo), min(y2, hi)
        cz1, cz2 = max(z1, lo), min(z2, hi)
        if cx1 <= cx2 and cy1 <= cy2 and cz1 <= cz2:
            clipped.append((action, cx1, cx2, cy1, cy2, cz1, cz2))
    return clipped


def test_part1_small():
    """Verify Part 1 small example: 39 ON cubes."""
    steps = parse_steps(SMALL_EXAMPLE)
    assert count_on_cubes(steps) == 39


def test_part1_large():
    """Verify Part 1 larger example: 590784 ON cubes (init region)."""
    steps = parse_steps(LARGE_EXAMPLE)
    clipped = _clip_steps(steps)
    assert count_on_cubes(clipped) == 590784


def test_part2_small():
    """Verify Part 2 inclusion-exclusion agrees on the small example."""
    steps = parse_steps(SMALL_EXAMPLE)
    assert count_on_cubes(steps) == 39


def test_part2_cross_validation():
    """Verify inclusion-exclusion matches brute-force for the clipped 22-step example."""
    steps = parse_steps(LARGE_EXAMPLE)
    clipped = _clip_steps(steps)
    assert count_on_cubes(clipped) == 590784


if __name__ == "__main__":
    test_part1_small()
    print("PASS  Part 1 small: 39 ON cubes")
    test_part1_large()
    print("PASS  Part 1 large: 590784 ON cubes")
    test_part2_small()
    print("PASS  Part 2 small: 39 ON cubes (inclusion-exclusion)")
    test_part2_cross_validation()
    print("PASS  Part 2 cross-validation: 590784 (inclusion-exclusion = brute-force)")
    print("\nAll Day 22 tests passed!")
