#!/usr/bin/env python3
"""Tests for Day 20 using the 9-tile example from the problem statement.

Part 1: corner tiles are 1171, 1951, 2971, 3079.
        Product = 20899048083289.
Part 2: water roughness (# cells not in sea monsters) = 273.
"""

from day20 import find_corners, get_edge_matches, parse_tiles
from day20_part2 import (
    MONSTER_SIZE,
    all_orientations,
    assemble_image,
    count_sea_monsters,
    strip_borders,
)

EXAMPLE = """\
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#
"""


def test_parse():
    """Verify parse_tiles yields 9 tiles with correct structure."""
    tiles = parse_tiles(EXAMPLE)
    assert len(tiles) == 9, f"Expected 9 tiles, got {len(tiles)}"
    assert 2311 in tiles
    assert len(tiles[2311]) == 10
    print("PASS  parse_tiles: 9 tiles parsed correctly")


def test_edge_matches():
    """Verify corner tiles 1171, 1951, 2971, 3079 are identified by edge matching."""
    tiles = parse_tiles(EXAMPLE)
    matches = get_edge_matches(tiles)
    corners = sorted(tid for tid in tiles if len(matches.get(tid, set())) == 2)
    assert corners == [1171, 1951, 2971, 3079], f"Got {corners}"
    print(f"PASS  edge_matches: corners = {corners}")


def test_part1():
    """Verify Part 1 example: corner tile product is 20899048083289."""
    tiles = parse_tiles(EXAMPLE)
    corners = find_corners(tiles)
    product = 1
    for c in corners:
        product *= c
    assert product == 20899048083289, f"Expected 20899048083289, got {product}"
    print(f"PASS  Part 1: product of corners = {product}")


def test_part2():
    """Verify Part 2 example: water roughness is 273 after finding sea monsters."""
    tiles = parse_tiles(EXAMPLE)
    placed = assemble_image(tiles)
    image = strip_borders(placed)
    assert len(image) == 24, f"Expected 24-row image, got {len(image)}"
    assert len(image[0]) == 24, f"Expected 24-col image, got {len(image[0])}"

    for oriented in all_orientations(image):
        monsters = count_sea_monsters(oriented)
        if monsters > 0:
            total_hash = sum(row.count("#") for row in oriented)
            roughness = total_hash - monsters * MONSTER_SIZE
            assert roughness == 273, f"Expected 273, got {roughness}"
            print(
                f"PASS  Part 2: roughness = {roughness} "
                f"({monsters} sea monsters found)"
            )
            return

    assert False, "No sea monsters found in any orientation"


if __name__ == "__main__":
    test_parse()
    test_edge_matches()
    test_part1()
    test_part2()
    print("\nAll Day 20 tests passed!")
