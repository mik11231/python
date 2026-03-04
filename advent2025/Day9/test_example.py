#!/usr/bin/env python3
"""Test Day 9 Part 1 with the example from the problem"""

# Example from problem
example_tiles = [
    (7, 1),
    (11, 1),
    (11, 7),
    (9, 7),
    (9, 5),
    (2, 5),
    (2, 3),
    (7, 3),
]

def solve_example():
    """Find largest rectangle in example."""
    n = len(example_tiles)
    print(f"Example: {n} red tiles")
    print(f"Tiles: {example_tiles}")
    
    max_area = 0
    best_pair = None
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = example_tiles[i]
            x2, y2 = example_tiles[j]
            
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            if area > max_area:
                max_area = area
                best_pair = ((x1, y1), (x2, y2))
                print(f"  New max: {best_pair[0]} to {best_pair[1]}, area = {area}")
    
    print(f"\nLargest rectangle: {best_pair[0]} to {best_pair[1]}")
    print(f"Area: {max_area} (expected: 50)")
    
    return max_area

if __name__ == "__main__":
    expected = 50
    actual = solve_example()
    if actual == expected:
        print("\nExample test PASSED!")
    else:
        print(f"\nExample test FAILED! Expected {expected}, got {actual}")





