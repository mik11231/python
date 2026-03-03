#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 21: Allergen Assessment (Part 1)

Each line lists ingredients and the allergens they might contain.  Each
allergen is found in exactly one ingredient, but an ingredient might contain
zero allergens.  Determine which ingredients *cannot* possibly contain any
allergen, then count how many times those safe ingredients appear across all
food lists.

Algorithm
---------
For every allergen, the ingredient that contains it must appear in *every*
food that lists that allergen.  Intersect the ingredient sets for each
allergen to narrow down the candidates.  Ingredients that appear in no
candidate set are safe.
"""

from pathlib import Path


def parse_foods(text: str) -> list[tuple[set[str], set[str]]]:
    """Parse input into a list of ``(ingredients, allergens)`` pairs."""
    foods: list[tuple[set[str], set[str]]] = []
    for line in text.strip().splitlines():
        parts = line.split(" (contains ")
        ingredients = set(parts[0].split())
        allergens = set(parts[1].rstrip(")").split(", "))
        foods.append((ingredients, allergens))
    return foods


def possible_allergen_map(
    foods: list[tuple[set[str], set[str]]],
) -> dict[str, set[str]]:
    """Map each allergen to the set of ingredients that might contain it."""
    possible: dict[str, set[str]] = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen in possible:
                possible[allergen] &= ingredients
            else:
                possible[allergen] = set(ingredients)
    return possible


def find_safe_ingredients(
    foods: list[tuple[set[str], set[str]]],
) -> set[str]:
    """Return ingredients that cannot contain any allergen."""
    possibly_dangerous: set[str] = set()
    for s in possible_allergen_map(foods).values():
        possibly_dangerous |= s
    all_ingredients: set[str] = set()
    for ingredients, _ in foods:
        all_ingredients |= ingredients
    return all_ingredients - possibly_dangerous


def solve(input_path: str = "advent2020/Day21/d21_input.txt") -> int:
    """Count total appearances of safe ingredients across all foods."""
    text = Path(input_path).read_text()
    foods = parse_foods(text)
    safe = find_safe_ingredients(foods)
    return sum(
        len(ingredients & safe) for ingredients, _ in foods
    )


if __name__ == "__main__":
    result = solve()
    print(f"Safe ingredient appearances: {result}")
