#!/usr/bin/env python3
"""Tests for Day 24 using the 20-line example from the problem statement.

Part 1: 10 black tiles after all flips.
Part 2 checkpoints: Day 1→15, Day 2→12, Day 3→25, Day 10→37,
                    Day 20→132, Day 100→2208.
"""

from day24 import parse_directions, identify_black_tiles
from day24_part2 import simulate, step

EXAMPLE_LINES = [
    "sesenwnenenewseeswwswswwnenewsewsw",
    "neeenesenwnwwswnenewnwwsewnenwseswesw",
    "seswneswswsenwwnwse",
    "nwnwneseeswswnenewneswwnewseswneseene",
    "swweswneswnenwsewnwneneseenw",
    "eesenwseswswnenwswnwnwsewwnwsene",
    "sewnenenenesenwsewnenwwwse",
    "wenwwweseeeweswwwnwwe",
    "wsweesenenewnwwnwsenewsenwwsesesenwne",
    "neeswseenwwswnwswswnw",
    "nenwswwsewswnenenewsenwsenwnesesenew",
    "enewnwewneswsewnwswenweswnenwsenwsw",
    "sweneswneswneneenwnewenewwneswswnese",
    "swwesenesewenwneswnwwneseswwne",
    "enesenwswwswneneswsenwnewswseenwsese",
    "wnwnesenesenenwwnenwsewesewsesesew",
    "nenewswnwewswnenesenwnesewesw",
    "eneswnwswnwsenenwnwnwwseeswneewsenese",
    "neswnwewnwnwseenwseesewsenwsweewe",
    "wseweeenwnesenwwwswnew",
]


def test_parse_directions():
    """Verify parse_directions correctly tokenizes hex directions."""
    dirs = parse_directions("esenee")
    assert dirs == ["e", "se", "ne", "e"], f"Got {dirs}"
    dirs2 = parse_directions("nwwswee")
    assert dirs2 == ["nw", "w", "sw", "e", "e"], f"Got {dirs2}"
    print("PASS  parse_directions")


def test_part1():
    """Verify Part 1 example: 10 black tiles after all flips."""
    black = identify_black_tiles(EXAMPLE_LINES)
    assert len(black) == 10, f"Expected 10 black tiles, got {len(black)}"
    print(f"PASS  Part 1: {len(black)} black tiles")


def test_part2_checkpoints():
    """Verify Part 2 simulation checkpoints: Day 1→15, 2→12, 3→25, 10→37, 20→132, 100→2208."""
    black = identify_black_tiles(EXAMPLE_LINES)
    checkpoints = {1: 15, 2: 12, 3: 25, 10: 37, 20: 132, 100: 2208}
    prev_day = 0
    for day in sorted(checkpoints):
        black = simulate(black, day - prev_day)
        prev_day = day
        expected = checkpoints[day]
        assert len(black) == expected, (
            f"Day {day}: expected {expected}, got {len(black)}"
        )
    print("PASS  Part 2 checkpoints: all match")
    print(f"PASS  Part 2: {len(black)} black tiles after 100 days")


if __name__ == "__main__":
    test_parse_directions()
    test_part1()
    test_part2_checkpoints()
    print("\nAll Day 24 tests passed!")
