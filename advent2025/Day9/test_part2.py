#!/usr/bin/env python3
"""Test Day 9 Part 2 with the example"""

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

def get_line_tiles(p1, p2):
    """
    Run `get_line_tiles` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: p1, p2.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    x1, y1 = p1
    x2, y2 = p2
    tiles = set()
    
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tiles.add((x1, y))
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tiles.add((x, y1))
    
    return tiles

def solve_example():
    """
    Run `solve_example` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    n = len(example_tiles)
    print(f"Example: {n} red tiles")
    
    red_set = set(example_tiles)
    
    # Build green tiles on lines
    green_set = set()
    for i in range(n):
        p1 = example_tiles[i]
        p2 = example_tiles[(i + 1) % n]
        line_tiles = get_line_tiles(p1, p2)
        green_set.update(line_tiles)
        green_set.discard(p1)
        green_set.discard(p2)
    
    print(f"Green tiles on lines: {len(green_set)}")
    
    # Fill interior using scanline
    all_x = [p[0] for p in example_tiles]
    all_y = [p[1] for p in example_tiles]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    
    print(f"Bounding box: ({min_x}, {min_y}) to ({max_x}, {max_y})")
    
    # Scanline fill
    for y in range(min_y, max_y + 1):
        intersections = []
        for i in range(n):
            x1, y1 = example_tiles[i]
            x2, y2 = example_tiles[(i + 1) % n]
            
            if (y1 <= y < y2) or (y2 <= y < y1):
                if y1 != y2:
                    x_intersect = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                    intersections.append(x_intersect)
        
        intersections.sort()
        
        for k in range(0, len(intersections), 2):
            if k + 1 < len(intersections):
                start_x = int(intersections[k]) + 1
                end_x = int(intersections[k + 1])
                for x in range(start_x, end_x + 1):
                    if (x, y) not in red_set and (x, y) not in green_set:
                        green_set.add((x, y))
    
    print(f"Total green tiles: {len(green_set)}")
    
    # Visualize
    print("\nGrid (R=red, G=green, .=other):")
    for y in range(max_y, min_y - 1, -1):
        line = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in red_set:
                line += "#"
            elif (x, y) in green_set:
                line += "X"
            else:
                line += "."
        print(f"{y:2} {line}")
    print("   " + "".join(str(x % 10) for x in range(min_x, max_x + 1)))
    
    # Find largest rectangle
    valid_tiles = red_set | green_set
    max_area = 0
    best_pair = None
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = example_tiles[i]
            x2, y2 = example_tiles[j]
            
            min_rect_x = min(x1, x2)
            max_rect_x = max(x1, x2)
            min_rect_y = min(y1, y2)
            max_rect_y = max(y1, y2)
            
            width = max_rect_x - min_rect_x + 1
            height = max_rect_y - min_rect_y + 1
            area = width * height
            
            if area <= max_area:
                continue
            
            # Check if all tiles in rectangle are valid
            valid = True
            for x in range(min_rect_x, max_rect_x + 1):
                for y in range(min_rect_y, max_rect_y + 1):
                    if (x, y) not in valid_tiles:
                        valid = False
                        break
                if not valid:
                    break
            
            if valid and area > max_area:
                max_area = area
                best_pair = ((x1, y1), (x2, y2))
                print(f"\nNew max: {best_pair[0]} to {best_pair[1]}, area = {area}")
    
    print(f"\nLargest rectangle area: {max_area} (expected: 24)")
    return max_area

if __name__ == "__main__":
    expected = 24
    actual = solve_example()
    if actual == expected:
        print("\nExample test PASSED!")
    else:
        print(f"\nExample test FAILED! Expected {expected}, got {actual}")





