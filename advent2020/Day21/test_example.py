#!/usr/bin/env python3
"""Tests for Day 21 using the example from the problem statement.

Four foods with three allergens (dairy, fish, soy).
Part 1: safe ingredients {kfcds, nhms, trh, sbzzf} appear 5 times total.
Part 2: dairy=mxmxvkd, fish=sqjhc, soy=fvjkl -> "mxmxvkd,sqjhc,fvjkl"
"""

from day21 import parse_foods, find_safe_ingredients
from day21_part2 import resolve_allergens, canonical_dangerous_list

EXAMPLE = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""


def test_parse():
    """Verify parse_foods correctly parses 4 foods with ingredients and allergens."""
    foods = parse_foods(EXAMPLE)
    assert len(foods) == 4
    assert foods[0] == ({"mxmxvkd", "kfcds", "sqjhc", "nhms"}, {"dairy", "fish"})
    print("PASS  parse_foods")


def test_part1():
    """Verify Part 1 example: safe ingredients appear 5 times total."""
    foods = parse_foods(EXAMPLE)
    safe = find_safe_ingredients(foods)
    assert safe == {"kfcds", "nhms", "trh", "sbzzf"}, f"Got safe={safe}"
    count = sum(len(ingredients & safe) for ingredients, _ in foods)
    assert count == 5, f"Expected 5 appearances, got {count}"
    print(f"PASS  Part 1: safe ingredients appear {count} times")


def test_part2():
    """Verify Part 2 example: canonical dangerous list is mxmxvkd,sqjhc,fvjkl."""
    foods = parse_foods(EXAMPLE)
    resolved = resolve_allergens(foods)
    assert resolved == {"dairy": "mxmxvkd", "fish": "sqjhc", "soy": "fvjkl"}, (
        f"Got {resolved}"
    )
    result = canonical_dangerous_list(foods)
    assert result == "mxmxvkd,sqjhc,fvjkl", f"Expected mxmxvkd,sqjhc,fvjkl, got {result}"
    print(f"PASS  Part 2: {result}")


if __name__ == "__main__":
    test_parse()
    test_part1()
    test_part2()
    print("\nAll Day 21 tests passed!")
