#!/usr/bin/env python3
"""Advent of Code 2025 - Day 9: Movie Theater"""

from pathlib import Path
def solve():
    """Solve Day 9 Part 1: Find largest rectangle using two red tiles as opposite corners."""
    # Read all red tile positions
    red_tiles = []
    with open(Path(__file__).with_name('d9_input.txt'), 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                red_tiles.append((x, y))
    
    n = len(red_tiles)
    print(f"Read {n} red tiles")
    
    # For each pair of red tiles, calculate the rectangle area
    max_area = 0
    best_pair = None
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            
            # Calculate rectangle area
            # The rectangle spans from min to max in both dimensions
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            if area > max_area:
                max_area = area
                best_pair = ((x1, y1), (x2, y2))
    
    if best_pair:
        print(f"Largest rectangle: {best_pair[0]} to {best_pair[1]}")
        print(f"Area: {max_area}")
    
    return max_area

if __name__ == "__main__":
    result = solve()
    print(f"\nLargest rectangle area: {result}")





