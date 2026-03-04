#!/usr/bin/env python3
"""Test Day 8 Part 1 with the example from the problem"""

import math

class UnionFind:
    """Union-Find (Disjoint Set) data structure for tracking circuits."""
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
    
    def get_circuit_sizes(self):
        sizes = []
        for i in range(len(self.parent)):
            if self.parent[i] == i:
                sizes.append(self.size[i])
        return sizes

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
    
    # Connect the 10 shortest pairs
    print("\nConnecting 10 shortest pairs:")
    for idx, (dist, i, j) in enumerate(pairs[:10], 1):
        connected = uf.union(i, j)
        status = "connected" if connected else "already in same circuit"
        print(f"  {idx}. Distance {dist:.2f}: box {i} <-> box {j} ({status})")
    
    # Get circuit sizes
    circuit_sizes = uf.get_circuit_sizes()
    circuit_sizes.sort(reverse=True)
    
    print(f"\nNumber of circuits: {len(circuit_sizes)}")
    print(f"Circuit sizes: {circuit_sizes}")
    print(f"Three largest: {circuit_sizes[:3]}")
    
    result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
    print(f"\nProduct: {result} (expected: 40)")
    
    return result

if __name__ == "__main__":
    expected = 40
    actual = solve_example()
    if actual == expected:
        print("\nExample test PASSED!")
    else:
        print(f"\nExample test FAILED! Expected {expected}, got {actual}")





