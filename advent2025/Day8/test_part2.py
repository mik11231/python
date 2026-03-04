#!/usr/bin/env python3
"""Test Day 8 Part 2 with the example from the problem"""

import math

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        
        return True
    
    def num_circuits(self):
        count = 0
        for i in range(len(self.parent)):
            if self.parent[i] == i:
                count += 1
        return count

def distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

# Example from problem
example_boxes = [
    (162, 817, 812),
    (57, 618, 57),
    (906, 360, 560),
    (592, 479, 940),
    (352, 342, 300),
    (466, 668, 158),
    (542, 29, 236),
    (431, 825, 988),
    (739, 650, 466),
    (52, 470, 668),
    (216, 146, 977),
    (819, 987, 18),
    (117, 168, 530),
    (805, 96, 715),
    (346, 949, 466),
    (970, 615, 88),
    (941, 993, 340),
    (862, 61, 35),
    (984, 92, 344),
    (425, 690, 689),
]

def solve_example():
    n = len(example_boxes)
    print(f"Example: {n} junction boxes")
    
    # Calculate all pairwise distances
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(example_boxes[i], example_boxes[j])
            pairs.append((dist, i, j))
    
    # Sort by distance
    pairs.sort()
    
    # Initialize union-find
    uf = UnionFind(n)
    
    # Connect pairs until all boxes are in one circuit
    print("\nConnecting pairs until all in one circuit...")
    last_connection = None
    connection_count = 0
    
    for dist, i, j in pairs:
        if uf.union(i, j):
            connection_count += 1
            num_circuits = uf.num_circuits()
            print(f"  Connection {connection_count}: box {i} ({example_boxes[i]}) <-> box {j} ({example_boxes[j]})")
            print(f"    Distance: {dist:.2f}, Circuits remaining: {num_circuits}")
            
            if num_circuits == 1:
                last_connection = (i, j)
                print(f"\nAll boxes connected! Last connection: box {i} <-> box {j}")
                break
    
    if last_connection is None:
        print("Error: Could not connect all boxes")
        return 0
    
    # Multiply X coordinates
    i, j = last_connection
    x1 = example_boxes[i][0]
    x2 = example_boxes[j][0]
    result = x1 * x2
    
    print(f"\nX coordinates: {x1} * {x2} = {result}")
    print(f"Expected: 25272 (216 * 117)")
    
    return result

if __name__ == "__main__":
    expected = 25272
    actual = solve_example()
    if actual == expected:
        print("\nExample test PASSED!")
    else:
        print(f"\nExample test FAILED! Expected {expected}, got {actual}")





