#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 21: Allergen Assessment (Part 2)

Determine exactly which ingredient contains which allergen.  Return the
*canonical dangerous ingredient list*: ingredients sorted alphabetically
by their allergen name, joined by commas.

Algorithm
---------
Iteratively resolve the allergen→ingredient mapping: any allergen with only
one candidate ingredient is assigned; that ingredient is then removed from
all other allergens' candidate sets.  Repeat until every allergen is resolved.
"""

from pathlib import Path

from day21 import parse_foods, possible_allergen_map


def resolve_allergens(
    foods: list[tuple[set[str], set[str]]],
) -> dict[str, str]:
    """Return a dict mapping each allergen to its ingredient."""
    possible = possible_allergen_map(foods)
    resolved: dict[str, str] = {}

    while possible:
        for allergen, candidates in list(possible.items()):
            if len(candidates) == 1:
                ingredient = next(iter(candidates))
                resolved[allergen] = ingredient
                del possible[allergen]
                for other in possible.values():
                    other.discard(ingredient)
                break

    return resolved


def canonical_dangerous_list(
    foods: list[tuple[set[str], set[str]]],
) -> str:
    """Return dangerous ingredients sorted by allergen, comma-separated."""
    resolved = resolve_allergens(foods)
    return ",".join(resolved[a] for a in sorted(resolved))


def solve(input_path: str = "advent2020/Day21/d21_input.txt") -> str:
    """Read input and return the canonical dangerous ingredient list."""
    text = Path(input_path).read_text()
    foods = parse_foods(text)
    return canonical_dangerous_list(foods)


if __name__ == "__main__":
    result = solve()
    print(f"Canonical dangerous ingredient list: {result}")
